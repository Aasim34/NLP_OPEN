"""
Hindi → English translation service.
Uses the Helsinki-NLP/opus-mt-hi-en transformer model from HuggingFace
to translate Devanagari Hindi text into English — fully offline.
"""

import re
from transformers import MarianMTModel, MarianTokenizer

# ---------------------------------------------------------------------------
# Model loading (runs once when the module is first imported)
# ---------------------------------------------------------------------------
_MODEL_NAME = "Helsinki-NLP/opus-mt-hi-en"

print(f"[hindi_to_english] Loading model '{_MODEL_NAME}' …  (first run downloads ~300 MB)")
_tokenizer = MarianTokenizer.from_pretrained(_MODEL_NAME)
_model = MarianMTModel.from_pretrained(_MODEL_NAME)
print("[hindi_to_english] Model loaded successfully.")


def _add_improved_punctuation(text: str) -> str:
    """
    Add improved punctuation to Hindi text to help the translation model
    understand sentence structure better.
    
    Steps:
    1. Add commas after common clause separators (है, हैं, था, थी, थे, हूँ)
       when not followed by conjunctions
    2. Ensure sentence ends with purna viram (।)
    3. Preserve existing punctuation
    """
    # Words after which comma should NOT be inserted
    no_comma_after = {
        "और", "या", "लेकिन", "मगर", "पर", "तो", "तब",
        "क्योंकि", "इसलिए", "वरना", "भी", "ही", "तक", "से"
    }
    
    # Split into words while preserving existing punctuation
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        # Check if word already has punctuation at end
        has_punctuation = word and word[-1] in ",।.!?"
        
        # Add comma after auxiliary verbs at clause boundaries
        if not has_punctuation and word in ("है", "हैं", "था", "थी", "थे", "हूँ", "हो"):
            # Check if next word exists and is not a conjunction
            if i + 1 < len(words):
                next_word = words[i + 1].rstrip(",।.!?")  # Strip any existing punctuation
                if next_word not in no_comma_after:
                    word = word + ","
        
        result.append(word)
    
    # Join and clean up any double spaces
    text = " ".join(result)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Ensure sentence ends with purna viram
    if text and text[-1] not in "।.!?":
        text += "।"
    
    return text


def translate(hindi_text: str) -> str:
    """
    Translate a Hindi (Devanagari) sentence into English using the
    local MarianMT transformer model.

    Args:
        hindi_text: A sentence in Devanagari script (from hinglish_to_hindi conversion).

    Returns:
        The English translation string.
    """
    # ========================================================================
    # DEBUG: Log the original Hindi sentence received
    # ========================================================================
    print(f"\n{'─'*60}")
    print(f"[TRANSLATION DEBUG]")
    print(f"  1. RECEIVED HINDI TEXT: '{hindi_text}'")
    
    # Add improved punctuation for better translation
    prepared = _add_improved_punctuation(hindi_text)
    print(f"  2. AFTER PUNCTUATION  : '{prepared}'")
    
    # ========================================================================
    # CRITICAL: This is the exact text sent to the translation model
    # ========================================================================
    print(f"  3. HINDI SENTENCE SENT TO TRANSLATION MODEL: '{prepared}'")
    print(f"{'─'*60}\n")
    
    # Tokenize the prepared Hindi input for the model
    inputs = _tokenizer(
        prepared,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )
    
    # Generate the translated token IDs with improved parameters
    translated_ids = _model.generate(
        **inputs,
        max_length=512,
        num_beams=4,           # Beam search for better quality
        early_stopping=True,   # Stop when all beams end
        no_repeat_ngram_size=3 # Avoid repetition
    )
    
    # Decode the token IDs back into a readable English string
    english_text = _tokenizer.decode(
        translated_ids[0],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )
    
    # Clean up and return
    return english_text.strip()
