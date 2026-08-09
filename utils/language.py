from enum import Enum
import re

class Language(Enum):
    HINDI = "hindi"
    HINGLISH = "hinglish"
    ENGLISH = "english"

HINDI_CHARS_RE = re.compile(r"[\u0900-\u097F]")
HINGLISH_KEYWORDS = ["kya", "hai", "nahi", "kaise", "kya\s", "kab", "bhai", "suna", "suna\b", "krna", "karna"]

def detect_language(text: str) -> Language:
    if not text or not text.strip():
        return Language.ENGLISH
    # If contains Devanagari characters assume Hindi
    if HINDI_CHARS_RE.search(text):
        return Language.HINDI
    # If Latin script but contains common Hinglish words, treat as Hinglish
    low = text.lower()
    count = sum(1 for k in HINGLISH_KEYWORDS if k in low)
    if count >= 1:
        return Language.HINGLISH
    # Default to English
    return Language.ENGLISH
