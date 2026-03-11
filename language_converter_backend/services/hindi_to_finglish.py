"""
Hindi → Finglish (Roman Hindi) conversion service.
Converts Devanagari Hindi text into natural, human-readable
Roman Hindi using a reverse lookup from the phonetic-fixes map
(so common words keep their natural Hinglish spelling), with
ITRANS transliteration as a fallback for unknown words.
"""

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from services.hinglish_to_hindi import _PHONETIC_FIXES

# ---------------------------------------------------------------------------
# Build reverse map: Devanagari → preferred natural Roman spelling.
# When multiple Roman spellings map to the same Devanagari word,
# the first entry in _PHONETIC_FIXES wins (via setdefault).
# ---------------------------------------------------------------------------
_DEVANAGARI_TO_ROMAN: dict[str, str] = {}
for _roman, _devanagari in _PHONETIC_FIXES.items():
    _DEVANAGARI_TO_ROMAN.setdefault(_devanagari, _roman)


def convert(hindi_text: str) -> str:
    """
    Convert a Devanagari Hindi sentence into Finglish
    (Romanised Hindi / Roman Hindi transliteration).

    Uses a reverse lookup of the phonetic-fixes map for natural
    Hinglish output, falling back to ITRANS for unknown words.

    Example:
        हेलो भाई कैसा है  →  Helo bhai kaisa hai

    Args:
        hindi_text: A sentence in Devanagari script.

    Returns:
        The Romanised (Finglish) version of the sentence.
    """
    # Strip Hindi punctuation — Finglish output should be clean
    clean = hindi_text.replace(",", "").replace("।", "").replace("!", "").replace("?", "")

    words = clean.split()
    finglish_words: list[str] = []

    for word in words:
        if word in _DEVANAGARI_TO_ROMAN:
            # Known word — use natural Hinglish spelling
            finglish_words.append(_DEVANAGARI_TO_ROMAN[word])
        else:
            # Fallback — ITRANS transliteration, lowercased
            roman = transliterate(word, sanscript.DEVANAGARI, sanscript.ITRANS)
            finglish_words.append(roman.lower())

    result = " ".join(finglish_words)

    # Capitalize only the first letter
    if result:
        result = result[0].upper() + result[1:]

    print(f"  [hindi_to_finglish] hindi='{hindi_text}' → finglish='{result}'")
    return result
