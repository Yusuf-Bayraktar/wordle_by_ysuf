"""Türkçe Wordle grafiksel kullanıcı arayüzü (Tkinter)."""
import tkinter as tk
from tkinter import messagebox
from typing import ClassVar

from wordle.dictionary import WordleDictionary
from wordle.game import LetterState, WordleGame
from wordle.turkish import TURKISH_KEYBOARD_LAYOUT, normalize_word


class WordleColors:
    """Gözü yormayan modern koyu tema renk paleti."""

    BG_DARK = "#181a20"          # Yumuşak antrasit arka plan
    HEADER_BG = "#1e222b"        # Üst bar arka planı

    # Harf kutusu renkleri
    CELL_BG_EMPTY = "#222630"     # Boş kutu dolgusu
    CELL_BORDER_EMPTY = "#343b49" # Boş kutu çerçevesi
    CELL_BG_ACTIVE = "#2b313e"    # Harf yazıldığında dolgu
    CELL_BORDER_ACTIVE = "#7e889b"# Harf yazıldığında çerçeve

    TEXT_COLOR = "#ffffff"
    TEXT_MUTED = "#9ba3b4"

    # Harf durum renkleri (Dengeli doygunluk)
    STATE_COLORS: ClassVar[dict[LetterState, str]] = {
        LetterState.CORRECT: "#388e3c",  # Dengeli zümrüt yeşili
        LetterState.PRESENT: "#d99b16",  # Sıcak amber sarısı
        LetterState.ABSENT: "#393e4a",   # Mat kayrak grisi
        LetterState.UNUSED: "#474e5d",   # Klavye tuş rengi
    }


class WordleUI:
    """Wordle Tkinter Arayüz Yöneticisi."""

    TILE_SIZE = 54  # Piksel bazında tam kare ölçüsü

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Wordle Türkçe")
        self.root.geometry("520x730")
        self.root.minsize(480, 680)
        self.root.config(bg=WordleColors.BG_DARK)

        self.dictionary = WordleDictionary()
        self.game: WordleGame | None = None
        self.current_guess: str = ""

        # UI bileşen referansları
        self.tile_frames: list[list[tk.Frame]] = []
        self.tile_labels: list[list[tk.Label]] = []
        self.key_buttons: dict[str, tk.Button] = {}
        self.message_label: tk.Label | None = None

        self._init_layout()
        self._bind_events()
        self.start_new_game()

    def _init_layout(self) -> None:
        """Arayüz bileşenlerini oluşturur ve yerleştirir."""
        # Üst Başlık ve Yeni Oyun Butonu
        header_frame = tk.Frame(self.root, bg=WordleColors.BG_DARK)
        header_frame.pack(pady=(18, 6), fill="x", padx=24)

        title_label = tk.Label(
            header_frame,
            text="WORDLE TÜRKÇE",
            font=("Segoe UI", 18, "bold"),
            bg=WordleColors.BG_DARK,
            fg=WordleColors.TEXT_COLOR,
        )
        title_label.pack(side="left")

        new_game_btn = tk.Button(
            header_frame,
            text="Yeni Oyun",
            font=("Segoe UI", 10, "bold"),
            bg="#2c323f",
            fg="#ffffff",
            activebackground="#3e4657",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5,
            bd=0,
            command=self.start_new_game,
        )
        new_game_btn.pack(side="right")

        # Bilgilendirme / Toast Mesajı Etiketi
        self.message_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=WordleColors.BG_DARK,
            fg="#f1f3f7",
            height=1,
        )
        self.message_label.pack(pady=(2, 6))

        # 6x5 Harf Matrisi (Tam Kare Grid)
        grid_container = tk.Frame(self.root, bg=WordleColors.BG_DARK)
        grid_container.pack(pady=4)

        for row in range(6):
            row_frames = []
            row_labels = []
            row_box = tk.Frame(grid_container, bg=WordleColors.BG_DARK)
            row_box.pack(pady=3)

            for _col in range(5):
                # Tam kare olması için sabit boyutlu Frame kullanıyoruz
                cell_frame = tk.Frame(
                    row_box,
                    width=self.TILE_SIZE,
                    height=self.TILE_SIZE,
                    bg=WordleColors.CELL_BORDER_EMPTY,
                    padx=2,
                    pady=2,
                )
                cell_frame.pack_propagate(False)
                cell_frame.pack(side="left", padx=3)

                lbl = tk.Label(
                    cell_frame,
                    text="",
                    font=("Segoe UI", 20, "bold"),
                    bg=WordleColors.CELL_BG_EMPTY,
                    fg=WordleColors.TEXT_COLOR,
                    relief="flat",
                )
                lbl.pack(expand=True, fill="both")

                row_frames.append(cell_frame)
                row_labels.append(lbl)

            self.tile_frames.append(row_frames)
            self.tile_labels.append(row_labels)

        # Sanal Klavye (Keyboard)
        keyboard_container = tk.Frame(self.root, bg=WordleColors.BG_DARK)
        keyboard_container.pack(pady=(16, 12), fill="x", padx=8)

        for row_keys in TURKISH_KEYBOARD_LAYOUT:
            row_frame = tk.Frame(keyboard_container, bg=WordleColors.BG_DARK)
            row_frame.pack(pady=3)

            for key in row_keys:
                is_wide = key in ("ENTER", "<-")
                btn = tk.Button(
                    row_frame,
                    text="⌫" if key == "<-" else key,
                    font=("Segoe UI", 9 if is_wide else 10, "bold"),
                    width=5 if is_wide else 3,
                    height=2,
                    bg=WordleColors.STATE_COLORS[LetterState.UNUSED],
                    fg=WordleColors.TEXT_COLOR,
                    activebackground="#5d6577",
                    activeforeground=WordleColors.TEXT_COLOR,
                    relief="flat",
                    cursor="hand2",
                    bd=0,
                    command=lambda k=key: self._handle_input(k),
                )
                btn.pack(side="left", padx=2)
                self.key_buttons[key] = btn

    def _bind_events(self) -> None:
        """Fiziksel klavye tuş vuruşlarını bağlar."""
        self.root.bind("<Key>", self._on_key_press)

    def start_new_game(self) -> None:
        """Yeni bir oyun oturumu başlatır."""
        target = self.dictionary.get_random_target()
        self.game = WordleGame(target_word=target, dictionary=self.dictionary)
        self.current_guess = ""
        self._show_message("")

        # Kutuları sıfırla
        for row in range(6):
            for col in range(5):
                frame = self.tile_frames[row][col]
                lbl = self.tile_labels[row][col]
                frame.config(bg=WordleColors.CELL_BORDER_EMPTY)
                lbl.config(
                    text="",
                    bg=WordleColors.CELL_BG_EMPTY,
                    fg=WordleColors.TEXT_COLOR,
                )

        # Klavye tuş renklerini sıfırla
        for btn in self.key_buttons.values():
            btn.config(
                bg=WordleColors.STATE_COLORS[LetterState.UNUSED],
                fg=WordleColors.TEXT_COLOR,
            )

    def _show_message(self, text: str, duration_ms: int = 2500) -> None:
        """Kullanıcıya geçici bildirim mesajı gösterir."""
        if self.message_label:
            self.message_label.config(text=text)
            if text and duration_ms > 0:
                self.root.after(duration_ms, lambda: self._clear_message_if_same(text))

    def _clear_message_if_same(self, text: str) -> None:
        if self.message_label and self.message_label.cget("text") == text:
            self.message_label.config(text="")

    def _on_key_press(self, event: tk.Event) -> None:
        """Fiziksel klavye olayını işler."""
        if not self.game or self.game.is_over:
            if event.keysym in ("Return", "space"):
                self.start_new_game()
            return

        if event.keysym in ("Return", "KP_Enter"):
            self._handle_input("ENTER")
        elif event.keysym in ("BackSpace", "Delete"):
            self._handle_input("<-")
        elif event.char:
            char_upper = normalize_word(event.char)
            if len(char_upper) == 1 and char_upper in self.key_buttons:
                self._handle_input(char_upper)

    def _handle_input(self, key: str) -> None:
        """Sanal veya fiziksel klavyeden gelen girdiyi yönetir."""
        if not self.game or self.game.is_over:
            return

        if key == "ENTER":
            self._submit_guess()
        elif key == "<-":
            if self.current_guess:
                self.current_guess = self.current_guess[:-1]
                self._update_current_row()
        else:
            if len(self.current_guess) < 5:
                self.current_guess += key
                self._update_current_row()

    def _update_current_row(self) -> None:
        """Yazılmakta olan mevcut satırın görünümünü günceller."""
        if not self.game:
            return

        row = len(self.game.guesses)
        if row >= 6:
            return

        for col in range(5):
            frame = self.tile_frames[row][col]
            lbl = self.tile_labels[row][col]
            if col < len(self.current_guess):
                char = self.current_guess[col]
                lbl.config(text=char, bg=WordleColors.CELL_BG_ACTIVE)
                frame.config(bg=WordleColors.CELL_BORDER_ACTIVE)
            else:
                lbl.config(text="", bg=WordleColors.CELL_BG_EMPTY)
                frame.config(bg=WordleColors.CELL_BORDER_EMPTY)

    def _submit_guess(self) -> None:
        """Mevcut tahmini değerlendirir."""
        if not self.game:
            return

        if len(self.current_guess) < 5:
            self._show_message("⚠️ Yetersiz harf! 5 harf giriniz.")
            return

        current_row = len(self.game.guesses)
        success, message, states = self.game.make_guess(self.current_guess)

        if not success:
            self._show_message(f"⚠️ {message}")
            return

        if states is None:
            return

        # Satırdaki harf kutularını renklendir
        for col, state in enumerate(states):
            frame = self.tile_frames[current_row][col]
            lbl = self.tile_labels[current_row][col]
            color = WordleColors.STATE_COLORS[state]
            frame.config(bg=color)
            lbl.config(bg=color, fg=WordleColors.TEXT_COLOR)

        # Sanal klavye tuş renklerini güncelle
        for char, state in self.game.keyboard_states.items():
            if char in self.key_buttons:
                self.key_buttons[char].config(
                    bg=WordleColors.STATE_COLORS[state],
                    fg=WordleColors.TEXT_COLOR,
                )

        # Tahmin kutusunu sıfırla
        self.current_guess = ""

        # Oyun bitti mi kontrolü
        if self.game.is_over:
            if self.game.is_won:
                attempt_num = len(self.game.guesses)
                msg = f"🎉 Muhteşem! {attempt_num}. denemede bildiniz!"
                self._show_message(msg, duration_ms=0)
                win_text = (
                    f"🎉 Kelimeyi {attempt_num}. denemede doğru bildiniz!\n\n"
                    f"Doğru Kelime: {self.game.target_word}"
                )
                messagebox.showinfo("Tebrikler!", win_text)
            else:
                self._show_message(f"❌ Doğru kelime: {self.game.target_word}", duration_ms=0)
                loss_text = (
                    "Üzgünüz, tahmin hakkınız bitti.\n\n"
                    f"Doğru Kelime: {self.game.target_word}"
                )
                messagebox.showinfo("Oyun Bitti", loss_text)


def run_app() -> None:
    """Uygulamayı başlatır."""
    root = tk.Tk()
    _app = WordleUI(root)
    root.mainloop()
