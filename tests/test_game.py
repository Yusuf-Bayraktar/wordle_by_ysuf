"""Wordle oyun motoru ve kural testleri."""
from wordle.game import LetterState, WordleGame, evaluate_guess


def test_evaluate_guess_all_correct():
    result = evaluate_guess("KALEM", "KALEM")
    assert result == [LetterState.CORRECT] * 5


def test_evaluate_guess_all_absent():
    result = evaluate_guess("KALEM", "GÜÇSÜ")
    assert result == [LetterState.ABSENT] * 5


def test_evaluate_guess_mixed_no_duplicates():
    # Target: KALEM, Guess: KELAM
    # K: CORRECT (0)
    # E: PRESENT (1, target index 3)
    # L: CORRECT (2)
    # A: PRESENT (3, target index 1)
    # M: CORRECT (4)
    result = evaluate_guess("KALEM", "KELAM")
    assert result == [
        LetterState.CORRECT,
        LetterState.PRESENT,
        LetterState.CORRECT,
        LetterState.PRESENT,
        LetterState.CORRECT,
    ]


def test_evaluate_guess_duplicate_letters_critical():
    # Target: KALEM (1 'E' at index 3)
    # Guess: ERKEK ('E' at index 0 and 3)
    # Correct Wordle Rule:
    # E(0): PRESENT (since E(3) is matched to target's E(3)) -> wait!
    # Let's trace:
    # 1. Pass: target[3] == guess[3] ('E' == 'E') -> CORRECT! remaining 'E' becomes 0.
    # 2. Pass: guess[0] is 'E', but remaining 'E' is 0 -> ABSENT!
    # R(1): ABSENT
    # K(2): PRESENT (target has 'K' at 0)
    # E(3): CORRECT
    # K(4): ABSENT (target has only 1 'K', consumed by guess[2])
    result = evaluate_guess("KALEM", "ERKEK")
    assert result == [
        LetterState.ABSENT,
        LetterState.ABSENT,
        LetterState.PRESENT,
        LetterState.CORRECT,
        LetterState.ABSENT,
    ]


def test_evaluate_guess_duplicate_in_target():
    # Target: KAZAK (K at 0,4; A at 1,3; Z at 2)
    # Guess: KAKAO
    # K(0): CORRECT
    # A(1): CORRECT
    # K(2): PRESENT (matched with remaining K at index 4)
    # A(3): CORRECT
    # O(4): ABSENT
    result = evaluate_guess("KAZAK", "KAKAO")
    assert result == [
        LetterState.CORRECT,
        LetterState.CORRECT,
        LetterState.PRESENT,
        LetterState.CORRECT,
        LetterState.ABSENT,
    ]


def test_wordle_game_lifecycle():
    game = WordleGame(target_word="KALEM")
    assert game.attempts_left == 6
    assert game.is_won is False
    assert game.is_over is False

    # Invalid length
    ok, msg, _ = game.make_guess("KALE")
    assert ok is False
    assert "5 harfli" in msg

    # Invalid word
    ok, msg, _ = game.make_guess("ZZZZZ")
    assert ok is False
    assert "sözlükte" in msg

    # Valid wrong guess
    ok, msg, states = game.make_guess("KELAM")
    assert ok is True
    assert game.attempts_left == 5
    assert states is not None

    # Check keyboard state
    assert game.keyboard_states["K"] == LetterState.CORRECT
    assert game.keyboard_states["E"] == LetterState.PRESENT

    # Winning guess
    ok, msg, states = game.make_guess("KALEM")
    assert ok is True
    assert game.is_won is True
    assert game.is_over is True
    assert "kazandınız" in msg.lower()
