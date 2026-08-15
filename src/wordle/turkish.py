"""Türkçe karakter dönüşüm ve normalizasyon yardımcı modülü."""

LOWER_TO_UPPER = {
    "i": "İ",
    "ı": "I",
    "ğ": "Ğ",
    "ü": "Ü",
    "ş": "Ş",
    "ö": "Ö",
    "ç": "Ç",
    "â": "A",
    "î": "İ",
    "û": "U",
}

UPPER_TO_LOWER = {
    "İ": "i",
    "I": "ı",
    "Ğ": "ğ",
    "Ü": "ü",
    "Ş": "ş",
    "Ö": "ö",
    "Ç": "ç",
    "Â": "a",
    "Î": "i",
    "Û": "u",
}

# Standart Türkçe klavye harfleri (Wordle klavye düzeni için)
TURKISH_KEYBOARD_LAYOUT = [
    ["E", "R", "T", "Y", "U", "I", "O", "P", "Ğ", "Ü"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ş", "İ"],
    ["ENTER", "Z", "C", "V", "B", "N", "M", "Ö", "Ç", "<-"],
]

TURKISH_ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def turkish_upper(text: str) -> str:
    """Metni Türkçe kurallarına göre büyük harfe dönüştürür."""
    chars = []
    for ch in text:
        if ch in LOWER_TO_UPPER:
            chars.append(LOWER_TO_UPPER[ch])
        else:
            chars.append(ch.upper())
    return "".join(chars)


def turkish_lower(text: str) -> str:
    """Metni Türkçe kurallarına göre küçük harfe dönüştürür."""
    chars = []
    for ch in text:
        if ch in UPPER_TO_LOWER:
            chars.append(UPPER_TO_LOWER[ch])
        else:
            chars.append(ch.lower())
    return "".join(chars)


def normalize_word(word: str) -> str:
    """Kelimeyi boşluklardan arındırır, şapkalı harfleri sadeleştirir ve büyük harfe çevirir."""
    word = word.strip()
    return turkish_upper(word)
