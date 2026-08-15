"""Arayüz başlatma ve temel UI bileşen testleri."""
import tkinter as tk

from wordle.ui import WordleUI


def test_ui_initialization():
    """WordleUI'ın hatasız başlatılabildiğini doğrula."""
    root = tk.Tk()
    try:
        app = WordleUI(root)
        assert app.game is not None
        assert len(app.tile_labels) == 6
        assert len(app.tile_labels[0]) == 5
        assert len(app.key_buttons) > 25
    finally:
        root.destroy()
