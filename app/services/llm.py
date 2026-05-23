from openai import OpenAI
from app.config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)
    return _client


def chat(prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 2048) -> str:
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""


def chat_stream(prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 2048):
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    stream = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
