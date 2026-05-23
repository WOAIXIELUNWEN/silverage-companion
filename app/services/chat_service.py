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


def classify_intent(message: str) -> str:
    """Classify user intent using LLM, with keyword fallback."""
    try:
        prompt = INTENT_PROMPT.format(message=message)
        result = chat(prompt, temperature=0.1, max_tokens=16).strip().lower()
        if result in ("chat", "health", "emergency"):
            return result
    except Exception:
        pass
    return classify_sync(message)


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
