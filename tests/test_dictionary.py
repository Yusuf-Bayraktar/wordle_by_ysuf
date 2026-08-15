"""Sözlük ve kelime doğrulama testleri."""
from wordle.dictionary import WordleDictionary


def test_dictionary_loading():
    d = WordleDictionary()
    assert len(d.valid_words) > 1000
    assert len(d.target_words) > 500


def test_is_valid_word():
    d = WordleDictionary()
    assert d.is_valid_word("KALEM") is True
    assert d.is_valid_word("kalem") is True
    assert d.is_valid_word("İPLİK") is True
    assert d.is_valid_word("XYZAB") is False
    assert d.is_valid_word("ÇOKUZUN") is False


def test_get_random_target():
    d = WordleDictionary()
    w1 = d.get_random_target(seed=42)
    w2 = d.get_random_target(seed=42)
    assert w1 == w2
    assert len(w1) == 5
    assert d.is_valid_word(w1) is True
