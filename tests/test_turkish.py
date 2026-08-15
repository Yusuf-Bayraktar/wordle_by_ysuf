"""Türkçe karakter ve dönüşüm testleri."""
from wordle.turkish import normalize_word, turkish_lower, turkish_upper


def test_turkish_upper():
    assert turkish_upper("kalem") == "KALEM"
    assert turkish_upper("iğne") == "İĞNE"
    assert turkish_upper("ışık") == "IŞIK"
    assert turkish_upper("ağaç") == "AĞAÇ"
    assert turkish_upper("şeker") == "ŞEKER"
    assert turkish_upper("öğüt") == "ÖĞÜT"
    assert turkish_upper("üzüm") == "ÜZÜM"


def test_turkish_lower():
    assert turkish_lower("KALEM") == "kalem"
    assert turkish_lower("İĞNE") == "iğne"
    assert turkish_lower("IŞIK") == "ışık"
    assert turkish_lower("AĞAÇ") == "ağaç"
    assert turkish_lower("ŞEKER") == "şeker"
    assert turkish_lower("ÖĞÜT") == "öğüt"
    assert turkish_lower("ÜZÜM") == "üzüm"


def test_normalize_word():
    assert normalize_word(" hâlâ ") == "HALA"
    assert normalize_word("kâtip") == "KATİP"
    assert normalize_word("mâkûl") == "MAKUL"
