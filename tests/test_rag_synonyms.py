import unittest
from urllib.parse import unquote_plus

from src.rag.engineering_synonyms import make_expanded_fts_query, make_loose_fts_query
from src.rag.law_article_metadata import parse_article_parts
from src.rag.local_kosha_rag import (
    DEFAULT_INDEX_PATH,
    build_law_article_query_seed,
    connect_db,
    make_fts_query,
    resolve_law_article_url,
    search_index,
)


class RagSynonymTests(unittest.TestCase):
    def test_live_query_builder_uses_synonym_expansion(self) -> None:
        fts_query = make_fts_query("부식 배관")
        self.assertEqual(fts_query, make_expanded_fts_query("부식 배관"))
        self.assertIn(" AND ", fts_query)
        self.assertIn('"corrosion"', fts_query)
        self.assertIn('"piping"', fts_query)

    def test_multiword_english_phrases_expand(self) -> None:
        fts_query = make_expanded_fts_query("pressure vessel remaining life assessment")
        self.assertIn('"pressure vessel"', fts_query)
        self.assertIn('"remaining life assessment"', fts_query)
        self.assertIn('"M-69"', fts_query)
        self.assertIn(" AND ", fts_query)

    def test_loose_query_builder_keeps_or_fallback(self) -> None:
        fts_query = make_loose_fts_query("pressure vessel remaining life assessment")
        self.assertIn('"pressure vessel"', fts_query)
        self.assertIn('"M-69"', fts_query)
        self.assertNotIn(" AND ", fts_query)

    def test_article_256_uses_stable_url_override(self) -> None:
        self.assertEqual(parse_article_parts("제256조 부식 방지"), ("0256", "00"))
        self.assertEqual(parse_article_parts("제4조의2 지방자치단체의 책무"), ("0004", "02"))

        seed = build_law_article_query_seed(
            raw_id="KOSHA04_002000002000004000000000256000",
            title="제256조 부식 방지",
            category="4",
        )
        self.assertIn("산업안전보건기준에 관한 규칙", seed)
        self.assertIn("제256조", seed)

        url = resolve_law_article_url(
            raw_id="KOSHA04_002000002000004000000000256000",
            title="제256조 부식 방지",
            category="4",
            filepath="",
        )
        decoded = unquote_plus(url or "")
        self.assertIn("law.go.kr", url or "")
        self.assertIn("산업안전보건기준에 관한 규칙", decoded)
        self.assertIn("제256조", decoded)

    def test_publication_case_remaining_life_retrieves_m69(self) -> None:
        if not DEFAULT_INDEX_PATH.exists():
            self.skipTest(f"missing index: {DEFAULT_INDEX_PATH}")

        conn = connect_db(DEFAULT_INDEX_PATH)
        try:
            hits = search_index(conn, "pressure vessel remaining life assessment", 5, discipline="vessel")
        finally:
            conn.close()

        self.assertTrue(any(hit.reference_code == "M-69-2012" for hit in hits))

    def test_publication_case_rbi_retrieves_cc23(self) -> None:
        if not DEFAULT_INDEX_PATH.exists():
            self.skipTest(f"missing index: {DEFAULT_INDEX_PATH}")

        conn = connect_db(DEFAULT_INDEX_PATH)
        try:
            hits = search_index(conn, "risk based inspection vessel", 5)
        finally:
            conn.close()

        self.assertTrue(any(hit.reference_code == "C-C-23-2026" for hit in hits))

    def test_publication_case_corrosion_retrieves_paper_references(self) -> None:
        if not DEFAULT_INDEX_PATH.exists():
            self.skipTest(f"missing index: {DEFAULT_INDEX_PATH}")

        conn = connect_db(DEFAULT_INDEX_PATH)
        try:
            hits = search_index(
                conn,
                "chloride sour service corrosion prevention piping occupational safety statute Article 256",
                10,
            )
        finally:
            conn.close()

        refs = {hit.reference_code for hit in hits}
        titles = {hit.title for hit in hits}
        self.assertIn("B-M-18-2026", refs)
        self.assertIn("C-C-75-2026", refs)
        self.assertTrue(any("256" in title for title in titles))


if __name__ == "__main__":
    unittest.main()
