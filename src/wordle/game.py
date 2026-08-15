"""Wordle çekirdek oyun motoru ve kural değerlendirme modülü."""
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum

from wordle.dictionary import WordleDictionary
from wordle.turkish import normalize_word


class LetterState(str, Enum):
    """Harf değerlendirme durumları."""

    CORRECT = "correct"  # Yeşil: Doğru harf, doğru konum
    PRESENT = "present"  # Sarı: Kelimede var, yanlış konum
    ABSENT = "absent"    # Gri: Kelimede yok (veya harf sayısı aşıldı)
    UNUSED = "unused"    # Henüz denenmedi


# Klavye güncelleme öncelik hiyerarşisi: CORRECT > PRESENT > ABSENT > UNUSED
STATE_PRIORITY = {
    LetterState.CORRECT: 3,
    LetterState.PRESENT: 2,
    LetterState.ABSENT: 1,
    LetterState.UNUSED: 0,
}


def evaluate_guess(target: str, guess: str) -> list[LetterState]:
    """
    Standart 2 aşamalı Wordle algoritması ile tahmini değerlendirir.

    1. Aşama: Tüm tam eşleşmeler (CORRECT / Yeşil) belirlenir ve harf havuzundan düşülür.
    2. Aşama: Kalan harfler için varlık kontrolü (PRESENT / Sarı) yapılır.
    """
    target = normalize_word(target)
    guess = normalize_word(guess)

    if len(target) != 5 or len(guess) != 5:
        raise ValueError("Hedef ve tahmin kelimeleri 5 harfli olmalıdır.")

    result: list[LetterState] = [LetterState.ABSENT] * 5
    remaining_counts: dict[str, int] = Counter(target)

    # 1. Aşama: Doğru konumdaki harfler (Yeşil)
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = LetterState.CORRECT
            remaining_counts[guess[i]] -= 1

    # 2. Aşama: Yanlış konumdaki var olan harfler (Sarı) ve olmayanlar (Gri)
    for i in range(5):
        if result[i] == LetterState.CORRECT:
            continue

        char = guess[i]
        if remaining_counts.get(char, 0) > 0:
            result[i] = LetterState.PRESENT
            remaining_counts[char] -= 1
        else:
            result[i] = LetterState.ABSENT

    return result


@dataclass
class GuessResult:
    """Tek bir tahminin sonucu."""

    word: str
    states: list[LetterState]


@dataclass
class WordleGame:
    """Türkçe Wordle oyun durumu ve mantığı."""

    target_word: str
    dictionary: WordleDictionary = field(default_factory=WordleDictionary)
    max_attempts: int = 6
    guesses: list[GuessResult] = field(default_factory=list)
    keyboard_states: dict[str, LetterState] = field(default_factory=dict)
    is_won: bool = False
    is_over: bool = False

    def __post_init__(self) -> None:
        self.target_word = normalize_word(self.target_word)

    @property
    def attempts_left(self) -> int:
        """Kalan tahmin hakkı."""
        return max(0, self.max_attempts - len(self.guesses))

    def make_guess(self, word: str) -> tuple[bool, str, list[LetterState] | None]:
        """
        Kullanıcının tahminini işler.

        Dönüş: (başarılı_mı, mesaj, harf_durumları_listesi)
        """
        if self.is_over:
            return False, "Oyun zaten bitti!", None

        normalized = normalize_word(word)

        if len(normalized) != 5:
            return False, "Kelime 5 harfli olmalıdır.", None

        if not self.dictionary.is_valid_word(normalized):
            return False, "Kelime sözlükte bulunamadı!", None

        states = evaluate_guess(self.target_word, normalized)
        self.guesses.append(GuessResult(word=normalized, states=states))

        # Klavye tuş renklerini güncelle (öncelik korumalı)
        for char, state in zip(normalized, states, strict=False):
            current_state = self.keyboard_states.get(char, LetterState.UNUSED)
            if STATE_PRIORITY[state] > STATE_PRIORITY[current_state]:
                self.keyboard_states[char] = state

        # Kazanma kontrolü
        if normalized == self.target_word:
            self.is_won = True
            self.is_over = True
            return True, "Tebrikler, kazandınız!", states

        # Kaybetme kontrolü
        if len(self.guesses) >= self.max_attempts:
            self.is_over = True
            return True, f"Oyun bitti! Doğru kelime: {self.target_word}", states

        return True, "Tahmin geçerli.", states
