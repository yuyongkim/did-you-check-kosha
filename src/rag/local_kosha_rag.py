from __future__ import annotations

import argparse
import gzip
import json
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence
from urllib.error import URLError
from urllib.request import Request, urlopen

from src.rag.engineering_synonyms import make_expanded_fts_query, make_loose_fts_query
from src.rag.law_article_metadata import build_law_article_metadata

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX_PATH = REPO_ROOT / "datasets" / "kosha_rag" / "kosha_local_rag.sqlite3"
DEFAULT_GUIDE_CHUNKS = REPO_ROOT / "datasets" / "kosha_guide" / "normalized" / "guide_chunks.jsonl.gz"
DEFAULT_LAW_ARTICLES = REPO_ROOT / "datasets" / "kosha" / "normalized" / "law_articles.json"


@dataclass
class SearchHit:
    doc_id: str
    source_type: str
    title: str
    reference_code: str
    score: float
    snippet: str
    url: str | None


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local KOSHA RAG (SQLite FTS + optional Ollama answer generation)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Build local retrieval index")
    p_build.add_argument("--index-path", default=str(DEFAULT_INDEX_PATH), help="SQLite index path")
    p_build.add_argument("--guide-chunks", default=str(DEFAULT_GUIDE_CHUNKS), help="guide_chunks.jsonl.gz path")
    p_build.add_argument("--law-articles", default=str(DEFAULT_LAW_ARTICLES), help="law_articles.json path")
    p_build.add_argument("--rebuild", action="store_true", help="Drop existing records and rebuild from scratch")

    p_query = sub.add_parser("query", help="Run retrieval query (optional local LLM answer)")
    p_query.add_argument("query", help="Natural language query")
    p_query.add_argument("--index-path", default=str(DEFAULT_INDEX_PATH), help="SQLite index path")
    p_query.add_argument("--top-k", type=int, default=8, help="Top-K hits")
    p_query.add_argument("--discipline", default="", help="Optional discipline filter (piping/vessel/rotating/...)")
    p_query.add_argument("--generate", action="store_true", help="Generate final answer with local Ollama")
    p_query.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/generate", help="Ollama generate endpoint")
    p_query.add_argument("--model", default="qwen2.5:7b-instruct", help="Ollama model name")
    p_query.add_argument("--max-context", type=int, default=5, help="Max retrieved chunks to include for generation")
    p_query.add_argument("--json-output", action="store_true", help="Print machine-readable JSON only")

    return parser.parse_args(argv)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def connect_db(path: Path) -> sqlite3.Connection:
    ensure_parent(path)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            source_type TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            reference_code TEXT,
            discipline TEXT,
            url TEXT,
            metadata_json TEXT
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
        USING fts5(
            id UNINDEXED,
            title,
            content,
            reference_code,
            tokenize='unicode61 remove_diacritics 2'
        );
        """
    )
    conn.commit()


def clear_index(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM documents")
    conn.execute("DELETE FROM documents_fts")
    conn.commit()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_jsonl_gz(path: Path) -> Iterable[Dict[str, Any]]:
    with gzip.open(path, mode="rt", encoding="utf-8") as stream:
        for line in stream:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                yield row


def build_law_article_query_seed(raw_id: str, title: str, category: str) -> str:
    metadata = build_law_article_metadata(raw_id=raw_id, title=title, category=category)
    return str(metadata.get("query_seed") or "")


def resolve_law_article_url(raw_id: str, title: str, category: str, filepath: str) -> str | None:
    metadata = build_law_article_metadata(raw_id=raw_id, title=title, category=category, filepath=filepath)
    return str(metadata.get("resolved_url") or "") or None


def infer_discipline(title: str, content: str) -> str:
    merged = f"{title} {content}".lower()
    if any(token in merged for token in ["배관", "piping", "corrosion", "api 570"]):
        return "piping"
    if any(token in merged for token in ["압력용기", "vessel", "api 510"]):
        return "vessel"
    if any(token in merged for token in ["회전기기", "compressor", "pump", "api 610", "api 617", "api 618"]):
        return "rotating"
    if any(token in merged for token in ["전기", "electrical", "arc flash"]):
        return "electrical"
    if any(token in merged for token in ["계장", "instrument", "sil", "iec 61511"]):
        return "instrumentation"
    return "common"


def build_documents(guide_chunks_path: Path, law_articles_path: Path) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []

    for row in iter_jsonl_gz(guide_chunks_path):
        chunk_id = str(row.get("chunk_id") or "").strip()
        title = str(row.get("title") or "").strip()
        content = str(row.get("text") or "").strip()
        guide_no = str(row.get("guide_no") or "").strip()
        source_file = str(row.get("source_file") or "").strip()
        if not chunk_id or not content:
            continue

        docs.append(
            {
                "id": f"guide:{chunk_id}",
                "source_type": "guide_chunk",
                "title": title or guide_no or "KOSHA guide chunk",
                "content": content,
                "reference_code": guide_no or "",
                "discipline": infer_discipline(title, content),
                "url": source_file or None,
                "metadata_json": json.dumps(
                    {
                        "page_start": row.get("page_start"),
                        "page_end": row.get("page_end"),
                        "ofanc_ymd": row.get("ofanc_ymd"),
                    },
                    ensure_ascii=False,
                ),
            }
        )

    law_rows = read_json(law_articles_path)
    if isinstance(law_rows, list):
        for row in law_rows:
            if not isinstance(row, dict):
                continue
            raw_id = str(row.get("id") or "").strip()
            title = str(row.get("title") or "").strip()
            content = str(row.get("content") or "").strip()
            if not raw_id or not content:
                continue
            category = str(row.get("category") or "")
            metadata = build_law_article_metadata(
                raw_id=raw_id,
                title=title,
                category=category,
                filepath=str(row.get("resolved_url") or row.get("direct_url") or row.get("filepath") or ""),
            )
            stable_url = str(metadata.get("resolved_url") or "") or None
            docs.append(
                {
                    "id": f"law:{raw_id}",
                    "source_type": "law_article",
                    "title": title or raw_id,
                    "content": content,
                    "reference_code": raw_id,
                    "discipline": infer_discipline(title, content),
                    "url": stable_url,
                    "metadata_json": json.dumps(
                        {
                            "category": category,
                            "keyword": row.get("keyword"),
                            "stable_url": stable_url,
                            "law_name": metadata.get("law_name"),
                            "article_number": metadata.get("article_number"),
                            "article_label": metadata.get("article_label"),
                            "query_seed": metadata.get("query_seed"),
                            "direct_url": row.get("direct_url") or metadata.get("direct_url") or stable_url,
                            "search_url": row.get("search_url") or metadata.get("search_url"),
                        },
                        ensure_ascii=False,
                    ),
                }
            )

    return docs


def upsert_documents(conn: sqlite3.Connection, rows: List[Dict[str, Any]]) -> None:
    conn.executemany(
        """
        INSERT OR REPLACE INTO documents
        (id, source_type, title, content, reference_code, discipline, url, metadata_json)
        VALUES (:id, :source_type, :title, :content, :reference_code, :discipline, :url, :metadata_json)
        """,
        rows,
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO documents_fts (id, title, content, reference_code)
        VALUES (:id, :title, :content, :reference_code)
        """,
        rows,
    )
    conn.commit()


def make_fts_query(query: str) -> str:
    return make_expanded_fts_query(query)


def make_plain_fts_query(query: str) -> str:
    tokens = [item.strip() for item in query.split() if item.strip()]
    if not tokens:
        return query.strip()
    return " OR ".join(f'"{token}"' for token in tokens)


def make_snippet(content: str, query: str, max_len: int = 240) -> str:
    text = " ".join(content.split())
    if len(text) <= max_len:
        return text
    terms = [item for item in query.split() if item]
    lowered = text.lower()
    idx = -1
    for term in terms:
        pos = lowered.find(term.lower())
        if pos >= 0:
            idx = pos
            break
    if idx < 0:
        return text[:max_len].rstrip() + "..."
    start = max(0, idx - max_len // 3)
    end = min(len(text), start + max_len)
    body = text[start:end].strip()
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{body}{suffix}"


def search_index_with_fts_query(
    conn: sqlite3.Connection,
    fts_query: str,
    query: str,
    top_k: int,
    discipline: str = "",
) -> List[SearchHit]:
    params: List[Any] = [fts_query]
    discipline_sql = ""
    if discipline.strip():
        discipline_sql = "AND d.discipline = ?"
        params.append(discipline.strip().lower())
    params.append(max(1, top_k))

    rows = conn.execute(
        f"""
        SELECT d.id, d.source_type, d.title, d.content, d.reference_code, d.url,
               bm25(documents_fts) AS rank
        FROM documents_fts
        JOIN documents d ON d.id = documents_fts.id
        WHERE documents_fts MATCH ?
        {discipline_sql}
        ORDER BY rank
        LIMIT ?
        """,
        params,
    ).fetchall()

    hits: List[SearchHit] = []
    for row in rows:
        content = str(row["content"] or "")
        rank = float(row["rank"] or 0.0)
        score = -rank
        hits.append(
            SearchHit(
                doc_id=str(row["id"]),
                source_type=str(row["source_type"]),
                title=str(row["title"]),
                reference_code=str(row["reference_code"] or ""),
                score=score,
                snippet=make_snippet(content, query),
                url=str(row["url"]) if row["url"] else None,
            )
        )
    return hits


def search_index(conn: sqlite3.Connection, query: str, top_k: int, discipline: str = "") -> List[SearchHit]:
    primary_query = make_fts_query(query)
    hits = search_index_with_fts_query(conn, primary_query, query, top_k, discipline=discipline)
    if hits:
        return hits

    fallback_query = make_loose_fts_query(query)
    if fallback_query == primary_query:
        return hits
    return search_index_with_fts_query(conn, fallback_query, query, top_k, discipline=discipline)


def build_prompt(query: str, hits: List[SearchHit]) -> str:
    context_blocks: List[str] = []
    for idx, hit in enumerate(hits, start=1):
        context_blocks.append(
            "\n".join(
                [
                    f"[{idx}] {hit.title}",
                    f"source_type: {hit.source_type}",
                    f"reference: {hit.reference_code}",
                    f"snippet: {hit.snippet}",
                    f"url: {hit.url or 'N/A'}",
                ]
            )
        )
    context = "\n\n".join(context_blocks)

    return (
        "You are an EPC regulatory assistant. Answer in Korean.\n"
        "Use only the context below. If evidence is insufficient, say so explicitly.\n"
        "Always include citations in [n] format that map to the context blocks.\n\n"
        f"Question:\n{query}\n\n"
        f"Context:\n{context}\n\n"
        "Answer format:\n"
        "1) 핵심 결론\n"
        "2) 근거 요약\n"
        "3) 규제/실무 주의사항\n"
    )


def generate_with_ollama(ollama_url: str, model: str, prompt: str) -> str:
    payload = json.dumps(
        {"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.1}},
        ensure_ascii=False,
    ).encode("utf-8")
    request = Request(
        ollama_url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=120) as response:  # noqa: S310
            body = response.read().decode("utf-8")
    except URLError as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc

    data = json.loads(body)
    if not isinstance(data, dict):
        raise RuntimeError("Invalid Ollama response format.")
    return str(data.get("response") or "").strip()


def run_build(args: argparse.Namespace) -> int:
    index_path = Path(args.index_path).resolve()
    guide_chunks = Path(args.guide_chunks).resolve()
    law_articles = Path(args.law_articles).resolve()
    if not guide_chunks.exists():
        raise RuntimeError(f"guide chunks not found: {guide_chunks}")
    if not law_articles.exists():
        raise RuntimeError(f"law articles not found: {law_articles}")

    conn = connect_db(index_path)
    try:
        init_schema(conn)
        if args.rebuild:
            clear_index(conn)
        docs = build_documents(guide_chunks, law_articles)
        upsert_documents(conn, docs)
    finally:
        conn.close()

    print("[DONE] Local RAG index build completed")
    print(f"- index_path: {index_path}")
    print(f"- documents: {len(docs)}")
    return 0


def run_query(args: argparse.Namespace) -> int:
    index_path = Path(args.index_path).resolve()
    if not index_path.exists():
        raise RuntimeError(f"index db not found: {index_path}. Run build command first.")

    conn = connect_db(index_path)
    try:
        hits = search_index(conn, args.query, args.top_k, discipline=args.discipline)
    finally:
        conn.close()

    answer: str | None = None
    if args.generate:
        context_hits = hits[: max(1, args.max_context)]
        if not context_hits:
            answer = "근거 문서가 부족하여 답변을 생성할 수 없습니다."
        else:
            prompt = build_prompt(args.query, context_hits)
            answer = generate_with_ollama(args.ollama_url, args.model, prompt)

    payload = {
        "query": args.query,
        "top_k": args.top_k,
        "discipline": args.discipline or None,
        "hits": [
            {
                "doc_id": hit.doc_id,
                "source_type": hit.source_type,
                "title": hit.title,
                "reference_code": hit.reference_code,
                "score": hit.score,
                "snippet": hit.snippet,
                "url": hit.url,
            }
            for hit in hits
        ],
        "answer": answer,
    }

    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    print(f"[query] {args.query}")
    print(f"[hits] {len(hits)}")
    for idx, hit in enumerate(hits, start=1):
        print(f"{idx}. [{hit.source_type}] {hit.title}")
        print(f"   ref={hit.reference_code} score={hit.score:.4f}")
        print(f"   {hit.snippet}")
        if hit.url:
            print(f"   url={hit.url}")

    if answer is not None:
        print("\n[answer]")
        print(answer or "Ollama returned an empty answer.")

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    args = parse_args(argv)
    if args.command == "build":
        return run_build(args)
    if args.command == "query":
        return run_query(args)
    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
