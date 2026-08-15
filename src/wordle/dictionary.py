"""Kelime listelerini yöneten ve sözlük doğrulaması yapan modül."""
import random
from pathlib import Path

from wordle.turkish import normalize_word

DATA_DIR = Path(__file__).parent / "data"
WORDS_FILE = DATA_DIR / "words_5.txt"
TARGETS_FILE = DATA_DIR / "targets_5.txt"


class WordleDictionary:
    """Türkçe Wordle sözlük yöneticisi."""

    def __init__(self, words_file: Path | None = None, targets_file: Path | None = None) -> None:
        self.words_file = words_file or WORDS_FILE
        self.targets_file = targets_file or TARGETS_FILE
        self.valid_words: set[str] = set()
        self.target_words: list[str] = []
        self._load_words()

    def _load_words(self) -> None:
        """Sözlük dosyalarını yükler."""
        if self.words_file.exists():
            content = self.words_file.read_text(encoding="utf-8")
            self.valid_words = {
                normalize_word(line)
                for line in content.splitlines()
                if len(line.strip()) == 5
            }

        if self.targets_file.exists():
            content = self.targets_file.read_text(encoding="utf-8")
            self.target_words = [
                normalize_word(line)
                for line in content.splitlines()
                if len(line.strip()) == 5
            ]
        else:
            self.target_words = sorted(list(self.valid_words))

        # Hedef kelimeler aynı zamanda geçerli kelimeler havuzunda da yer almalıdır
        self.valid_words.update(self.target_words)

    def is_valid_word(self, word: str) -> bool:
        """Kelimenin 5 harfli ve sözlükte kayıtlı olup olmadığını denetler."""
        normalized = normalize_word(word)
        if len(normalized) != 5:
            return False
        return normalized in self.valid_words

    def get_random_target(self, seed: int | None = None) -> str:
        """Rastgele bir hedef kelime seçer."""
        if not self.target_words:
            if not self.valid_words:
                raise ValueError("Kelime havuzu boş!")
            return random.choice(sorted(list(self.valid_words)))

        rng = random.Random(seed) if seed is not None else random
        return rng.choice(self.target_words)
