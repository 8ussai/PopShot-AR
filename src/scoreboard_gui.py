import tkinter as tk
import sqlite3
import config
import os
import threading
from PIL import Image, ImageTk 

class Scoreboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scores Board")
        self.geometry("400x720")
        self.configure(bg="#88bbce") 
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        img = Image.open(config.LOGO_IMAGE)   
        img = img.resize((80, 80), Image.Resampling.LANCZOS)  
        self.logo_img = ImageTk.PhotoImage(img)

        logo_label = tk.Label(self, image=self.logo_img, bg="#88bbce")
        logo_label.pack(pady=(20, 10))

        title = tk.Label(self, text="PopShot AR", font=("DynaPuff", 40, "bold"),
                         fg="#115587", bg="#88bbce")
        title.pack(pady=(10, 5))

        dev = tk.Label(self, text="DEVELOPED BY\nQUSSAI ABU SHEHADEH",
                       font=("Night Holiday", 30, "bold"), fg="#0b3250", bg="#88bbce")
        dev.pack(pady=(0, 30))

        header_frame = tk.Frame(self, bg="#88bbce")
        header_frame.pack(pady=5)
        tk.Label(header_frame, text="PLAYER", font=("Rinder Spring Demo", 16, "bold"),
                 fg="gold", bg="#115587", width=14, height=2).grid(row=0, column=0, padx=5)
        tk.Label(header_frame, text="SCORE", font=("Rinder Spring Demo", 16, "bold"),
                 fg="gold", bg="#115587", width=6, height=2).grid(row=0, column=1, padx=5)

        self.rows = []
        for i in range(4):
            frame = tk.Frame(self, bg="#88bbce")
            frame.pack(pady=5)
            player_lbl = tk.Label(frame, text="", font=("Angkor", 12, "bold"),
                                  fg="white", bg="#115587", width=14, height=2)
            player_lbl.grid(row=0, column=0, padx=5)
            score_lbl = tk.Label(frame, text="", font=("Angkor", 12, "bold"),
                                 fg="white", bg="#115587", width=6, height=2)
            score_lbl.grid(row=0, column=1, padx=5)
            self.rows.append((player_lbl, score_lbl))

        self.update_scores_periodically()

    def update_scores_periodically(self):
        conn = sqlite3.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name, score FROM scores ORDER BY id DESC LIMIT 5")
        scores = cur.fetchall()
        conn.close()

        for i, (player_lbl, score_lbl) in enumerate(self.rows):
            if i < len(scores):
                player_lbl.config(text=scores[i][0])
                score_lbl.config(text=str(scores[i][1]))
            else:
                player_lbl.config(text="")
                score_lbl.config(text="")

        self.after(1000, self.update_scores_periodically)

    def on_close(self):
        os._exit(0)

def run_scoreboard():
    t = threading.Thread(target=lambda: Scoreboard().mainloop(), daemon=True)
    t.start()
