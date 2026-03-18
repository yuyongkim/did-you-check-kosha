import { KoshaRagQueryRequest, KoshaRagQueryResponse } from "@/lib/rag/types";

export async function queryLocalKoshaRag(
  request: KoshaRagQueryRequest,
): Promise<KoshaRagQueryResponse> {
  const response = await fetch("/api/rag/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    let detail = `RAG query failed: ${response.status}`;
    try {
      const body = (await response.json()) as { error?: string; detail?: string };
      if (body.error) detail = body.error;
      if (body.detail) detail = body.detail;
    } catch {
      // no-op
    }
    throw new Error(detail);
  }

  return (await response.json()) as KoshaRagQueryResponse;
}
