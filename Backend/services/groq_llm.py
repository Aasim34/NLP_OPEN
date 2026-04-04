"""
Lightweight GROQ LLM integration helper.

This module provides a single `query` function that calls the GROQ API
using the `GROQ_API_KEY` and `GROQ_MODEL` environment variables.

If those variables are not set the function returns a helpful message
instead of raising so the backend remains robust in development.
"""
from __future__ import annotations

import json
import os
from typing import Optional

import requests


def _extract_text_from_response(j: dict) -> Optional[str]:
    # Groq OpenAI-compatible response shape:
    # {
    #   "choices": [{"message": {"content": "..."}}],
    #   ...
    # }
    if not isinstance(j, dict):
        return None
    choices = j.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message.get("content")
            if isinstance(first.get("text"), str):
                return first.get("text")

    if isinstance(j.get("output_text"), str):
        return j.get("output_text")

    if isinstance(j.get("text"), str):
        return j.get("text")

    if isinstance(j.get("result"), str):
        return j.get("result")

    # Last resort: return pretty-printed JSON
    try:
        return json.dumps(j, ensure_ascii=False)
    except Exception:
        return None


def query(prompt: str, model: Optional[str] = None, api_key: Optional[str] = None) -> str:
    """Query the GROQ API and return a text response.

    The function expects either explicit `api_key` and `model` arguments
    or the `GROQ_API_KEY` / `GROQ_MODEL` environment variables to be set.

    Returns a string with the LLM output, or a short error/help message when
    the environment is not configured or the request fails.
    """
    api_key = api_key or os.getenv("GROQ_API_KEY")
    model = model or os.getenv("GROQ_MODEL")

    if not api_key or not model:
        return "[GROQ LLM] GROQ_API_KEY or GROQ_MODEL not configured"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return only the final user-facing answer. Do not include explanations, labels, or markdown fences."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 128,
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        return f"[GROQ LLM] Request failed: {exc}"

    try:
        j = resp.json()
    except Exception:
        return resp.text[:200]

    text = _extract_text_from_response(j)
    if text:
        return text.strip()

    # If the API schema changes, return a short diagnostic string so the
    # caller can decide whether to fall back.
    return "[GROQ LLM] No usable text returned from API"
