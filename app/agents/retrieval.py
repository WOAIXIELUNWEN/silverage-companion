import json
import os
from difflib import SequenceMatcher

KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_base.json")


def _load_knowledge() -> list[dict]:
    if not os.path.exists(KNOWLEDGE_PATH):
        return []
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search(query: str, top_k: int = 3) -> list[dict]:
    """Simple keyword + similarity search over the health knowledge base."""
    entries = _load_knowledge()
    if not entries:
        return []

    scored = []
    query_lower = query.lower()
    for entry in entries:
        keywords = entry.get("keywords", [])
        text = entry.get("question", "") + " " + entry.get("answer", "")
        text_lower = text.lower()

        score = 0
        for kw in keywords:
            if kw in query_lower:
                score += 3
        score += SequenceMatcher(None, query_lower, text_lower).ratio() * 2

        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:top_k]]


def format_context(results: list[dict]) -> str:
    if not results:
        return "（未找到相关健康知识）"
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(f"{i}. 问：{r['question']}\n   答：{r['answer']}")
    return "\n".join(parts)
