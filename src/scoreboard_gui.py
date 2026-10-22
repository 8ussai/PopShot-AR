import tkinter as tk
from PIL import Image, ImageTk

import config
import database
import fonts

BG = "#88bbce"
CELL_BG = "#115587"


class Scoreboard(tk.Tk):
    """Score window. It has no mainloop of its own: the game calls pump() every frame,
    which keeps Tkinter on the main thread (required on macOS)."""

    def __init__(self):
        fonts.load_fonts()  # must happen before Tk starts so it sees the fonts
        super().__init__()
        self.closed = False
        self.title("Scores Board")
        self.geometry("400x720")
        self.configure(bg=BG)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        img = Image.open(config.LOGO_IMAGE).resize((80, 80), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        tk.Label(self, image=self.logo_img, bg=BG).pack(pady=(20, 10))

        tk.Label(self, text="PopShot AR", font=("DynaPuff", 40, "bold"),
                 fg=CELL_BG, bg=BG).pack(pady=(10, 5))

        tk.Label(self, text="DEVELOPED BY\nQUSSAI ABU SHEHADEH",
                 font=("Night Holiday", 30, "bold"), fg="#0b3250", bg=BG).pack(pady=(0, 30))

        header_frame = tk.Frame(self, bg=BG)
        header_frame.pack(pady=5)
        tk.Label(header_frame, text="PLAYER", font=("Rinder Spring Demo", 16, "bold"),
                 fg="gold", bg=CELL_BG, width=14, height=2).grid(row=0, column=0, padx=5)
        tk.Label(header_frame, text="SCORE", font=("Rinder Spring Demo", 16, "bold"),
                 fg="gold", bg=CELL_BG, width=6, height=2).grid(row=0, column=1, padx=5)

        self.rows = []
        for _ in range(config.SCOREBOARD_ROWS):
            frame = tk.Frame(self, bg=BG)
            frame.pack(pady=5)
            player_lbl = tk.Label(frame, text="", font=("Angkor", 12, "bold"),
                                  fg="white", bg=CELL_BG, width=14, height=2)
            player_lbl.grid(row=0, column=0, padx=5)
            score_lbl = tk.Label(frame, text="", font=("Angkor", 12, "bold"),
                                 fg="white", bg=CELL_BG, width=6, height=2)
            score_lbl.grid(row=0, column=1, padx=5)
            self.rows.append((player_lbl, score_lbl))

        self.refresh()

    def refresh(self):
        scores = database.get_top_scores(config.SCOREBOARD_ROWS)
        for i, (player_lbl, score_lbl) in enumerate(self.rows):
            name, score = scores[i] if i < len(scores) else ("", "")
            player_lbl.config(text=name)
            score_lbl.config(text=str(score))

    def pump(self):
        """Process pending window events. Call once per game frame."""
        if not self.closed:
            self.update()

    def on_close(self):
        self.closed = True
        self.destroy()
