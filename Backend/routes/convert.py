"""
API route for the /convert endpoint.
Accepts a Hinglish sentence and returns Hindi, Finglish, and English outputs.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import asyncio
from typing import Optional
import json

from services import hinglish_to_hindi, hindi_to_finglish, hindi_to_english
import services.groq_llm as groq_llm

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class ConvertRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Hinglish input sentence")


class ConvertResponse(BaseModel):
    hindi: str
    finglish: str
    english: str
    llm_output: Optional[str] = None


# ---------------------------------------------------------------------------
# POST /convert
# ---------------------------------------------------------------------------
@router.post("/convert", response_model=ConvertResponse)
async def convert(request: ConvertRequest):
    """
    Convert a Hinglish (code-mixed Hindi + English) sentence into:
        - Pure Hindi (Devanagari)
        - Finglish (Roman Hindi transliteration)
        - English translation

    The entire pipeline runs locally — no external APIs are called.
    """
    try:
        from utils.tokenizer import normalize

        print(f"\n{'='*60}")
        print(f"[pipeline] INPUT TEXT      : '{request.text}'")
        print(f"[pipeline] NORMALIZED TEXT : '{normalize(request.text)}'")

        # Step 1 — Normalize + Hinglish → pure Hindi (Devanagari)
        hindi = hinglish_to_hindi.convert(request.text)
        print(f"[pipeline] HINDI OUTPUT    : '{hindi}'")

        # Step 2 — Hindi → Finglish (Roman transliteration)
        finglish = hindi_to_finglish.convert(hindi)
        print(f"[pipeline] FINGLISH OUTPUT : '{finglish}'")

        # Step 3 — Hindi → English (local transformer model)
        english = hindi_to_english.translate(hindi)
        print(f"[pipeline] ENGLISH OUTPUT  : '{english}'")

        # Step 4 — Optional: Query external LLM (GROQ) for an additional
        # output. This uses the GROQ_API_KEY and GROQ_MODEL environment vars.
        llm_prompt = (
            f"Original input: {request.text}\n"
            f"Hindi: {hindi}\n"
            f"Finglish: {finglish}\n"
            f"English: {english}\n\n"
            "Provide only one concise alternative English rendering. "
            "Return only the final sentence, with no explanation, no labels, and no extra lines."
        )

        try:
            raw_llm_output = await asyncio.to_thread(groq_llm.query, llm_prompt)
        except Exception as exc:
            raw_llm_output = f"[LLM ERROR] {exc}"

        print(f"[pipeline] RAW LLM OUTPUT  : '{raw_llm_output}'")

        # Sanitize LLM output: hide technical errors and return only
        # the user-facing text. If the LLM helper returned an error
        # prefixed with [GROQ LLM] or similar, we don't forward it to
        # the frontend — keep the `llm_output` empty instead.
        llm_output = ""
        if raw_llm_output:
            # Hide known error markers (case-insensitive)
            lower = raw_llm_output.lower().strip()
            if lower.startswith("[groq llm]") or lower.startswith("[llm error]") or "request failed" in lower or "failed to resolve" in lower:
                llm_output = ""
            else:
                # Try to detect JSON and extract useful text
                try:
                    parsed = json.loads(raw_llm_output)
                    if isinstance(parsed, dict):
                        extracted = groq_llm._extract_text_from_response(parsed)
                        llm_output = extracted or ""
                    elif isinstance(parsed, str):
                        llm_output = parsed
                    else:
                        llm_output = ""
                except Exception:
                    # Not JSON — assume raw string is fine
                    llm_output = raw_llm_output

        # Keep only the first non-empty line so the frontend shows only
        # the direct answer and not any extra explanation text.
        if llm_output:
            lines = [line.strip() for line in llm_output.splitlines() if line.strip()]
            llm_output = lines[0] if lines else ""

        # If LLM produced nothing (network error or sanitized error),
        # provide a harmless fallback so the frontend always shows a
        # concise assistant message. We use the local `english` output
        # as a reliable fallback (keeps UI informative without leaking
        # technical errors).
        if not llm_output:
            llm_output = english

        print(f"[pipeline] LLM OUTPUT      : '{llm_output}'")
        print(f"{'='*60}\n")

        return ConvertResponse(hindi=hindi, finglish=finglish, english=english, llm_output=llm_output)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing error: {exc}")
