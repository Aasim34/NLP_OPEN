"""
API route for the /convert endpoint.
Accepts a Hinglish sentence and returns Hindi, Finglish, and English outputs.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services import hinglish_to_hindi, hindi_to_finglish, hindi_to_english

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
        print(f"{'='*60}\n")

        return ConvertResponse(hindi=hindi, finglish=finglish, english=english)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing error: {exc}")
