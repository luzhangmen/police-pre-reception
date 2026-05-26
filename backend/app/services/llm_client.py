import json
import logging
import os
from typing import Any

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "kimi-k2.6"
_DEFAULT_TEMPERATURE = 1.0

_client: Any | None = None


def _get_client() -> Any | None:
    global _client
    if _client is None:
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            return None
        from openai import OpenAI

        base_url = os.getenv("LLM_BASE_URL", "https://api.moonshot.cn/v1")
        _client = OpenAI(api_key=api_key, base_url=base_url)
    return _client


def call_llm(
    user_prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    temperature: float = _DEFAULT_TEMPERATURE,
    json_mode: bool = False,
) -> str:
    """Call the LLM and return raw text response."""
    if os.getenv("PYTEST_CURRENT_TEST"):
        return ""
    client = _get_client()
    if client is None:
        logger.warning("LLM_API_KEY not set, skipping LLM call")
        return ""
    model = os.getenv("LLM_MODEL", _DEFAULT_MODEL)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    kwargs: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    try:
        response = client.chat.completions.create(**kwargs)
    except Exception as exc:
        logger.warning("LLM request failed: %s", exc)
        return ""

    content = response.choices[0].message.content
    return content or ""


def call_llm_json(
    user_prompt: str,
    system_prompt: str = "You are a helpful assistant. Reply with valid JSON only.",
    temperature: float = _DEFAULT_TEMPERATURE,
) -> dict:
    """Call the LLM and parse the response as JSON. Returns an empty dict on failure."""
    raw = call_llm(
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        json_mode=True,
    )
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}
