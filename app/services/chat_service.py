import os
import uuid
from app.agents.intent import classify_sync, INTENT_PROMPT
from app.agents.companion import (
    COMPANION_SYSTEM_PROMPT,
    HEALTH_SYSTEM_PROMPT,
    EMERGENCY_SYSTEM_PROMPT,
)
from app.agents.retrieval import search, format_context
from app.agents.safety import basic_filter, SAFETY_PROMPT
from app.services.llm import chat, chat_stream


def _is_demo_mode() -> bool:
    key = os.getenv("MIMO_API_KEY", "")
    return not key or key.startswith("your-")


def classify_intent(message: str) -> str:
    """Classify user intent using LLM, with keyword fallback."""
    if _is_demo_mode():
        return classify_sync(message)
    try:
        prompt = INTENT_PROMPT.format(message=message)
        result = chat(prompt, temperature=0.1, max_tokens=16).strip().lower()
        if result in ("chat", "health", "emergency"):
            return result
    except Exception:
        pass
    return classify_sync(message)


def _demo_reply(message: str, intent: str) -> str:
    """Generate a response without LLM, using local KB and templates."""
    if intent == "emergency":
        return (
            "请您保持冷静！我强烈建议您立即拨打120急救电话，"
            "或联系家人、邻居寻求帮助。在等待急救期间，请尽量"
            "保持平静，不要随意移动身体。您的安全最重要！🚨"
        )
    elif intent == "health":
        results = search(message, top_k=3)
        if results:
            parts = [f"关于您的问题，我找到了以下建议：\n"]
            for i, r in enumerate(results, 1):
                parts.append(f"{i}. {r['answer']}")
            parts.append("\n以上仅供参考，具体请咨询医生。祝您健康！🌸")
            return "\n".join(parts)
        else:
            return (
                "您提的健康问题很好。不过我的知识库里暂时没有这方面的详细信息。"
                "建议您咨询专业医生获取更准确的建议。去社区医院问问也是个好选择！🏥"
            )
    else:
        return (
            "谢谢您跟我聊天！每天保持好心情对身体很重要哦。"
            "今天有什么开心的事想跟我分享吗？或者有什么心事想聊聊？"
            "我会一直在这里陪着您 🌿"
        )


def get_system_prompt(intent: str, message: str) -> str:
    if intent == "emergency":
        return EMERGENCY_SYSTEM_PROMPT
    elif intent == "health":
        results = search(message, top_k=3)
        context = format_context(results)
        return HEALTH_SYSTEM_PROMPT.format(context=context)
    else:
        return COMPANION_SYSTEM_PROMPT


def generate_reply(message: str, intent: str) -> str:
    if _is_demo_mode():
        return _demo_reply(message, intent)

    system_prompt = get_system_prompt(intent, message)
    response = chat(message, system_prompt=system_prompt, temperature=0.7, max_tokens=512)

    if intent == "health":
        try:
            safety_prompt = SAFETY_PROMPT.format(response=response)
            response = chat(safety_prompt, temperature=0.1, max_tokens=512)
        except Exception:
            response = basic_filter(response)

    return response


def generate_reply_stream(message: str, intent: str):
    if _is_demo_mode():
        reply = _demo_reply(message, intent)
        for ch in reply:
            yield ch
        return

    system_prompt = get_system_prompt(intent, message)
    full_response = ""
    for token in chat_stream(message, system_prompt=system_prompt, temperature=0.7, max_tokens=512):
        full_response += token
        yield token

    if intent == "health":
        full_response = basic_filter(full_response)


def process_message(message: str, session_id: str = None) -> dict:
    if session_id is None:
        session_id = uuid.uuid4().hex[:16]

    intent = classify_intent(message)
    reply = generate_reply(message, intent)

    return {
        "session_id": session_id,
        "intent": intent,
        "reply": reply,
    }


def process_message_stream(message: str, session_id: str = None):
    if session_id is None:
        session_id = uuid.uuid4().hex[:16]

    intent = classify_intent(message)
    system_prompt = get_system_prompt(intent, message)

    # Yield metadata first
    yield {"type": "meta", "session_id": session_id, "intent": intent}

    full_response = ""
    for token in chat_stream(message, system_prompt=system_prompt, temperature=0.7, max_tokens=512):
        full_response += token
        yield {"type": "token", "content": token}

    if intent == "health":
        full_response = basic_filter(full_response)

    yield {"type": "done", "full_response": full_response}
