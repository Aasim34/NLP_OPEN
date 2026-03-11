"""
Hinglish → Hindi conversion service.
Converts a code-mixed Hinglish sentence into Devanagari Hindi using:
  1. A phonetic normalization map for common casual romanization words
     (corrects cases where ITRANS gives wrong results for informal spelling).
  2. ITRANS phonetic transliteration as fallback for unknown words.

This is NOT a translation dictionary — every mapping is the SAME word
transliterated from informal Roman spelling to its correct Devanagari script.
"""

import re

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from utils.tokenizer import tokenize

# ---------------------------------------------------------------------------
# Spelling normalization map
# Corrects common informal / misspelled romanizations BEFORE the phonetic
# lookup or ITRANS transliteration runs.
# e.g. "tyari" → "tayari", "kese" → "kaise"
# ---------------------------------------------------------------------------
_SPELLING_NORMALIZE: dict[str, str] = {
    # tayari / taiyari variants
    "tyari": "tayari", "taiyari": "tayari", "taiyaari": "tayari",
    "teyari": "tayari", "teiyari": "tayari",
    # kaise variants
    "kese": "kaise", "kaese": "kaise", "kaesa": "kaisa",
    # other common misspellings
    "accha": "achha", "acha": "achha",
    "achhi": "achi", "achi": "achi",
    "bhai": "bhai", "bhi": "bhi",
    "chize": "cheeze", "chiz": "cheez",
    "dusra": "doosra", "dusri": "doosri",
    "hmare": "hamare", "hmari": "hamari", "hmara": "hamara",
    "tumhre": "tumhare", "tumhri": "tumhari",
    "krega": "karega", "krna": "karna", "krenge": "karenge",
    "krunga": "karunga", "krungi": "karungi",
    "smjha": "samjha", "smjho": "samjho", "smajh": "samajh",
    "pdhai": "padhai", "pdhna": "padhna", "pdho": "padho",
    "likhna": "likhna", "lkhna": "likhna",
    "milna": "milna", "mlna": "milna",
    "bolna": "bolna", "blna": "bolna",
    "sunna": "sunna", "snna": "sunna",
    "dekha": "dekha", "dkha": "dekha",
    "zaruri": "zaroori", "zaruri": "zaroori",
    "mushkl": "mushkil",
    "pankha": "pankha",
    "kbhi": "kabhi", "hmesa": "hamesha", "hmesha": "hamesha",
    "srdi": "sardi", "grmi": "garmi",
    "jldii": "jaldi", "jldi": "jaldi",
}


# ---------------------------------------------------------------------------
# Phonetic normalization map
# Corrects common casual romanization → Devanagari where the ITRANS scheme
# produces incorrect results.  e.g. "bhai" in ITRANS = भै (wrong),
# correct = भाई.
# ---------------------------------------------------------------------------
_PHONETIC_FIXES: dict[str, str] = {
    # --- Greetings & expressions ---
    "hello": "हेलो", "hi": "हाय", "hey": "हे", "bye": "बाय",
    "ok": "ओके", "okay": "ओके",
    "please": "प्लीज़", "sorry": "सॉरी",
    "thank": "थैंक", "thanks": "थैंक्स",
    "welcome": "वेलकम", "namaste": "नमस्ते", "namaskar": "नमस्कार",

    # --- Pronouns ---
    "mai": "मैं", "main": "मैं", "mein": "में", "me": "में",
    "mujhe": "मुझे", "mujhko": "मुझको", "mujhse": "मुझसे",
    "tumhe": "तुम्हें", "tumhko": "तुमको", "tumse": "तुमसे",
    "hume": "हमें", "humko": "हमको", "humse": "हमसे",
    "use": "उसे", "usko": "उसको", "usse": "उससे",
    "unhe": "उन्हें", "unko": "उनको", "unse": "उनसे",
    "hum": "हम", "tu": "तू", "tum": "तुम",
    "aap": "आप", "ap": "आप",
    "ye": "यह", "yeh": "यह", "wo": "वो", "woh": "वो",
    "yaha": "यहाँ", "yahan": "यहाँ", "waha": "वहाँ", "wahan": "वहाँ",
    "kya": "क्या", "koi": "कोई", "kuch": "कुछ",
    "sab": "सब", "sabhi": "सभी",

    # --- Possessives ---
    "mera": "मेरा", "mere": "मेरे", "meri": "मेरी",
    "tera": "तेरा", "tere": "तेरे", "teri": "तेरी",
    "tumhara": "तुम्हारा", "tumhare": "तुम्हारे", "tumhari": "तुम्हारी",
    "hamara": "हमारा", "hamare": "हमारे", "hamari": "हमारी",
    "iska": "इसका", "iski": "इसकी", "iske": "इसके",
    "uska": "उसका", "uski": "उसकी", "uske": "उसके",
    "unka": "उनका", "unki": "उनकी", "unke": "उनके",
    "apka": "आपका", "aapka": "आपका",
    "apki": "आपकी", "aapki": "आपकी",
    "apna": "अपना", "apni": "अपनी", "apne": "अपने",

    # --- Postpositions ---
    "ka": "का", "ki": "की", "ke": "के", "ko": "को",
    "se": "से", "par": "पर", "pe": "पर", "ne": "ने", "tak": "तक",

    # --- Auxiliary verbs ---
    "hai": "है", "hain": "हैं", "ho": "हो",
    "tha": "था", "thi": "थी", "the": "थे",
    "hota": "होता", "hoti": "होती", "hote": "होते",
    "hoga": "होगा", "hogi": "होगी", "honge": "होंगे",
    "hua": "हुआ", "hui": "हुई", "hue": "हुए",

    # --- Common verbs ---
    "kar": "कर", "karo": "करो", "karna": "करना",
    "karta": "करता", "karti": "करती", "karte": "करते",
    "kiya": "किया", "kiye": "किये",
    "karega": "करेगा", "karegi": "करेगी", "karenge": "करेंगे",
    "ja": "जा", "jao": "जाओ", "jana": "जाना",
    "jata": "जाता", "jati": "जाती", "jate": "जाते",
    "gaya": "गया", "gayi": "गयी", "gaye": "गये",
    "jayega": "जाएगा", "jayegi": "जाएगी",
    "aa": "आ", "aao": "आओ", "aana": "आना",
    "aata": "आता", "aati": "आती", "aate": "आते",
    "aaya": "आया", "aayi": "आयी", "aaye": "आये",
    "le": "ले", "lo": "लो", "lena": "लेना",
    "leta": "लेता", "leti": "लेती", "lete": "लेते",
    "liya": "लिया", "liye": "लिये",
    "de": "दे", "do": "दो", "dena": "देना",
    "deta": "देता", "deti": "देती", "dete": "देते",
    "diya": "दिया", "diye": "दिये",
    "dekh": "देख", "dekho": "देखो", "dekhna": "देखना", "dekha": "देखा",
    "bol": "बोल", "bolo": "बोलो", "bolna": "बोलना", "bola": "बोला",
    "sun": "सुन", "suno": "सुनो", "sunna": "सुनना", "suna": "सुना",
    "padh": "पढ़", "padho": "पढ़ो", "padhna": "पढ़ना",
    "likh": "लिख", "likho": "लिखो", "likhna": "लिखना",
    "kha": "खा", "khao": "खाओ", "khana": "खाना",
    "pi": "पी", "piyo": "पियो", "peena": "पीना",
    "baith": "बैठ", "baitho": "बैठो", "baithna": "बैठना",
    "chal": "चल", "chalo": "चलो", "chalna": "चलना",
    "rakh": "रख", "rakho": "रखो",
    "mil": "मिल", "milna": "मिलना", "mila": "मिला",
    "milega": "मिलेगा", "milegi": "मिलेगी",
    "samajh": "समझ", "samjho": "समझो",
    "soch": "सोच", "socho": "सोचो",
    "ruk": "रुक", "ruko": "रुको",
    "bana": "बना", "banao": "बनाओ",
    "chahiye": "चाहिए", "chahie": "चाहिए",
    "chahta": "चाहता", "chahte": "चाहते",
    "chahti": "चाहती", "chahta": "चाहता",
    "chahunga": "चाहूँगा", "chahungi": "चाहूँगी",

    # --- Common nouns ---
    "bhai": "भाई", "bhaiya": "भैया",
    "behen": "बहन", "bahen": "बहन", "didi": "दीदी",
    "maa": "माँ", "papa": "पापा",
    "dost": "दोस्त", "yaar": "यार", "log": "लोग",
    "aadmi": "आदमी", "ladka": "लड़का", "ladki": "लड़की",
    "bachcha": "बच्चा", "baccha": "बच्चा", "bachche": "बच्चे",
    "ghar": "घर", "paani": "पानी", "pani": "पानी",
    "kaam": "काम", "baat": "बात", "din": "दिन", "raat": "रात",
    "subah": "सुबह", "shaam": "शाम", "sham": "शाम",
    "kal": "कल", "aaj": "आज", "abhi": "अभी",
    "dil": "दिल", "pyaar": "प्यार", "pyar": "प्यार",
    "zindagi": "ज़िंदगी", "duniya": "दुनिया",
    "cheez": "चीज़", "jagah": "जगह", "tarah": "तरह",
    "matlab": "मतलब", "wajah": "वजह",
    "paisa": "पैसा", "paise": "पैसे",
    "chai": "चाय", "roti": "रोटी", "doodh": "दूध", "dudh": "दूध",
    "khushi": "खुशी", "dukh": "दुख",
    "galti": "गलती", "madad": "मदद", "koshish": "कोशिश",
    "mushkil": "मुश्किल", "pata": "पता",
    "naukri": "नौकरी", "padhai": "पढ़ाई",
    "sadak": "सड़क", "rasta": "रास्ता", "raasta": "रास्ता",

    # --- Adjectives / adverbs ---
    "achha": "अच्छा", "accha": "अच्छा", "acha": "अच्छा",
    "achi": "अच्छी", "acchi": "अच्छी",
    "bura": "बुरा", "buri": "बुरी",
    "bada": "बड़ा", "badi": "बड़ी", "bade": "बड़े",
    "chota": "छोटा", "chhota": "छोटा", "choti": "छोटी",
    "naya": "नया", "nayi": "नयी",
    "purana": "पुराना", "purani": "पुरानी",
    "bahut": "बहुत", "bohot": "बहुत", "boht": "बहुत",
    "thoda": "थोड़ा", "thodi": "थोड़ी",
    "zyada": "ज़्यादा", "jyada": "ज़्यादा",
    "sahi": "सही", "galat": "गलत",
    "theek": "ठीक", "thik": "ठीक",
    "kaisa": "कैसा", "kaisi": "कैसी", "kaise": "कैसे",
    "itna": "इतना", "itni": "इतनी", "itne": "इतने",
    "taiyar": "तैयार", "tayar": "तैयार",
    "khush": "खुश",

    # --- Negation & conjunctions ---
    "nahi": "नहीं", "nahin": "नहीं", "nai": "नहीं",
    "na": "ना", "mat": "मत",
    "aur": "और", "ya": "या",
    "lekin": "लेकिन", "magar": "मगर",
    "kyunki": "क्योंकि", "kyuki": "क्योंकि",
    "agar": "अगर", "to": "तो", "toh": "तो",
    "bhi": "भी", "hi": "ही",
    "sirf": "सिर्फ़", "bas": "बस",
    "phir": "फिर", "fir": "फिर",
    "warna": "वरना", "isliye": "इसलिए",

    # --- Question words ---
    "kaun": "कौन", "kon": "कौन", "kab": "कब",
    "kaha": "कहाँ", "kahan": "कहाँ",
    "kyun": "क्यों", "kyu": "क्यों",
    "kitna": "कितना", "kitni": "कितनी", "kitne": "कितने",

    # --- Time / place / direction ---
    "pehle": "पहले", "pahle": "पहले", "baad": "बाद",
    "saath": "साथ", "sath": "साथ",
    "andar": "अंदर", "bahar": "बाहर", "upar": "ऊपर",
    "neeche": "नीचे", "niche": "नीचे",
    "aage": "आगे", "peeche": "पीछे",
    "paas": "पास", "door": "दूर", "dur": "दूर",
    "hamesha": "हमेशा", "kabhi": "कभी",
    "jaldi": "जल्दी", "der": "देर",
    "zaroor": "ज़रूर", "zarur": "ज़रूर",
    "shayad": "शायद", "bilkul": "बिल्कुल",
    "idhar": "इधर", "udhar": "उधर",

    # --- Numbers ---
    "ek": "एक", "teen": "तीन", "chaar": "चार",
    "paanch": "पाँच", "panch": "पाँच",
    "saat": "सात", "aath": "आठ", "nau": "नौ", "das": "दस",
    "sau": "सौ", "hazaar": "हज़ार", "hazar": "हज़ार", "lakh": "लाख",

    # --- English loanwords (phonetic Devanagari, not translation) ---
    "meeting": "मीटिंग", "office": "ऑफिस",
    "school": "स्कूल", "college": "कॉलेज",
    "phone": "फ़ोन", "mobile": "मोबाइल",
    "computer": "कंप्यूटर", "laptop": "लैपटॉप",
    "internet": "इंटरनेट", "email": "ईमेल",
    "message": "मैसेज", "call": "कॉल",
    "movie": "मूवी", "game": "गेम", "party": "पार्टी",
    "hotel": "होटल", "hospital": "हॉस्पिटल",
    "doctor": "डॉक्टर", "police": "पुलिस",
    "ticket": "टिकट", "train": "ट्रेन",
    "bus": "बस", "car": "कार", "bike": "बाइक",
    "bank": "बैंक", "shop": "शॉप", "market": "मार्केट",
    "report": "रिपोर्ट", "project": "प्रोजेक्ट",
    "company": "कंपनी", "team": "टीम",
    "class": "क्लास", "exam": "एग्ज़ाम", "exams": "एग्ज़ाम्स", "test": "टेस्ट",
    "tayari": "तैयारी", "tayyari": "तैयारी", "tyaari": "तैयारी",
    "tayyar": "तैयार", "tayaar": "तैयार",
    "zaroori": "ज़रूरी", "jaroori": "ज़रूरी",
    "doosra": "दूसरा", "doosri": "दूसरी", "doosre": "दूसरे",
    "karunga": "करूँगा", "karungi": "करूँगी",
    "pankha": "पंखा",
    "samajhna": "समझना", "samjha": "समझा", "samjhi": "समझी",
    "sochna": "सोचना", "socha": "सोचा", "sochi": "सोची",
    "milna": "मिलना", "mili": "मिली", "mile": "मिले",
    "chalna": "चलना", "chala": "चला", "chali": "चली", "chale": "चले",
    "rakhna": "रखना", "rakha": "रखा", "rakhi": "रखी", "rakhe": "रखे",
    "sunna": "सुनना", "suni": "सुनी", "sune": "सुने",
    "bolna": "बोलना", "boli": "बोली", "bole": "बोले",
    "likhna": "लिखना", "likha": "लिखा", "likhi": "लिखी", "likhe": "लिखे",
    "padhna": "पढ़ना", "padha": "पढ़ा", "padhi": "पढ़ी", "padhe": "पढ़े",
    "kharidna": "खरीदना", "khareed": "खरीद", "khareeda": "खरीदा", "khareedi": "खरीदी",
    "bechna": "बेचना", "becha": "बेचा", "bechi": "बेची",
    "job": "जॉब", "salary": "सैलरी", "interview": "इंटरव्यू",
    "problem": "प्रॉब्लम", "idea": "आइडिया", "plan": "प्लान",
    "time": "टाइम", "date": "डेट",
    "birthday": "बर्थडे", "gift": "गिफ्ट",
    "coffee": "कॉफ़ी", "food": "फ़ूड",
    "music": "म्यूज़िक", "song": "सॉन्ग",
    "video": "वीडियो", "photo": "फ़ोटो", "camera": "कैमरा",
    "brother": "ब्रदर", "sister": "सिस्टर",
    "friend": "फ्रेंड", "family": "फ़ैमिली",
    "love": "लव", "life": "लाइफ",
    "happy": "हैप्पी", "sad": "सैड",
    "good": "गुड", "bad": "बैड", "best": "बेस्ट",
    "nice": "नाइस", "great": "ग्रेट",
    "right": "राइट", "wrong": "रॉन्ग",
    "fast": "फ़ास्ट", "slow": "स्लो",
    "new": "न्यू", "old": "ओल्ड", "latest": "लेटेस्ट",
    "big": "बिग", "small": "स्मॉल",
    "sir": "सर", "madam": "मैडम",
    "manager": "मैनेजर", "customer": "कस्टमर",
    "service": "सर्विस", "order": "ऑर्डर",
    "delivery": "डिलीवरी", "payment": "पेमेंट",
    "online": "ऑनलाइन", "password": "पासवर्ड",
    "number": "नंबर", "address": "एड्रेस",
    "weather": "वेदर", "summer": "समर", "winter": "विंटर",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_devanagari(word: str) -> bool:
    """Return True if the word already contains Devanagari characters."""
    return bool(re.search(r"[\u0900-\u097F]", word))


def _is_latin(word: str) -> bool:
    """Return True if the word is composed of Latin letters only."""
    return bool(re.match(r"^[a-zA-Z]+$", word))


def _transliterate_to_devanagari(word: str) -> str:
    """
    Fallback: Phonetically transliterate a Roman-script word into
    Devanagari using the ITRANS scheme.
    """
    return transliterate(word, sanscript.ITRANS, sanscript.DEVANAGARI)


def convert(sentence: str) -> str:
    """
    Convert a Hinglish (Hindi + English mixed) sentence into
    Devanagari Hindi.

    Processing steps:
        1. Tokenize and normalize the input.
        2. For each token:
            a. Check phonetic normalization map (fixes ITRANS errors).
            b. Already Devanagari → keep as-is.
            c. Latin script → ITRANS transliteration (fallback).
            d. Other (numbers, punctuation) → pass through.
        3. Reconstruct and return the Hindi sentence.

    Args:
        sentence: The raw Hinglish input string.

    Returns:
        A Devanagari Hindi sentence string.
    """
    tokens = tokenize(sentence)

    # --- Pre-step: normalize misspelled romanizations ---
    normalized_tokens = []
    for t in tokens:
        lower = t.lower()
        normalized_tokens.append(_SPELLING_NORMALIZE.get(lower, lower))

    print(f"  [hinglish_to_hindi] raw_tokens={tokens}")
    print(f"  [hinglish_to_hindi] normalized ={normalized_tokens}")

    hindi_tokens: list[str] = []

    for word in normalized_tokens:
        lower = word.lower()

        # 1. Phonetic normalization map — handles common words ITRANS
        #    would get wrong (e.g. "bhai" → भाई not भै)
        if lower in _PHONETIC_FIXES:
            hindi_tokens.append(_PHONETIC_FIXES[lower])

        # 2. Already in Devanagari — keep unchanged
        elif _is_devanagari(word):
            hindi_tokens.append(word)

        # 3. Latin script — ITRANS transliteration as fallback
        elif _is_latin(word):
            hindi_tokens.append(_transliterate_to_devanagari(word))

        # 4. Numbers, punctuation, symbols — pass through
        else:
            hindi_tokens.append(word)

    raw_hindi = " ".join(hindi_tokens)

    # --- Post-step: add basic Hindi punctuation for better structure ---
    result = _add_hindi_punctuation(raw_hindi)

    print(f"  [hinglish_to_hindi] tokens={tokens} → hindi='{result}'")
    return result


# ---------------------------------------------------------------------------
# Hindi punctuation helper
# ---------------------------------------------------------------------------

# Words after which a comma should NOT be inserted (conjunctions / particles)
_NO_COMMA_AFTER = {
    "और", "या", "लेकिन", "मगर", "पर", "तो",
    "क्योंकि", "इसलिए", "वरना", "भी", "ही", "तक",
}


def _add_hindi_punctuation(text: str) -> str:
    """
    Insert lightweight punctuation into a Hindi sentence to mark
    clause boundaries.  Adds a comma after auxiliary verbs
    (है / हैं / था / थी / थे) when they sit at a clause boundary
    (i.e. the next word is NOT a conjunction or particle).
    """
    words = text.split()
    result: list[str] = []

    for i, word in enumerate(words):
        result.append(word)
        # Insert comma after auxiliary verbs at clause boundaries
        if word in ("है", "हैं", "था", "थी", "थे") and i + 1 < len(words):
            if words[i + 1] not in _NO_COMMA_AFTER:
                result[-1] = word + ","

    return " ".join(result)
