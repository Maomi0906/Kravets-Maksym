import tkinter as tk
import json
import random
import os
import math


try:
    from PIL import Image, ImageTk, ImageDraw
    PILLOW_AVAILABLE = True
except Exception:
    PILLOW_AVAILABLE = False


COLORS = {
    "bg": "#0f3460",
    "panel": "#16213e",
    "accent": "#e94560",
    "secondary": "#00d2ff",
    "text": "#ffffff",
    "slider_track": "#0a192f",
}

FONT_MAIN = ("Helvetica", 12)
FONT_BOLD = ("Helvetica", 14, "bold")
FONT_TITLE = ("Helvetica", 32, "bold")

class ModernSlider(tk.Canvas):
    def __init__(self, parent, label_text, color_hex, command=None, **kwargs):
        super().__init__(parent, width=350, height=70, bg=COLORS["panel"], highlightthickness=0, **kwargs)
        self.command = command
        self.color_hex = color_hex
        self.value = 0
        
        self.bar_y = 25
        self.bar_height = 6
        self.knob_radius = 9
        
        self.create_text(175, 55, text=label_text, fill=color_hex, font=("Helvetica", 14, "bold"), anchor="center")
        
        self.bar_start_x, self.bar_end_x = 40, 310
        self.bar_length = self.bar_end_x - self.bar_start_x
        
        self.create_line(self.bar_start_x, self.bar_y, self.bar_end_x, self.bar_y, fill=COLORS["slider_track"], width=self.bar_height, capstyle="round")
        self.progress_line = self.create_line(self.bar_start_x, self.bar_y, self.bar_start_x, self.bar_y, fill=color_hex, width=self.bar_height, capstyle="round")
        self.knob = self.create_oval(self.bar_start_x - self.knob_radius, self.bar_y - self.knob_radius, self.bar_start_x + self.knob_radius, self.bar_y + self.knob_radius, fill=color_hex, outline="white", width=2)
        
        self.bind("<B1-Motion>", self._move_knob)
        self.bind("<Button-1>", self._move_knob)

    def _move_knob(self, event):
        x = max(self.bar_start_x, min(event.x, self.bar_end_x))
        self.coords(self.knob, x - self.knob_radius, self.bar_y - self.knob_radius, x + self.knob_radius, self.bar_y + self.knob_radius)
        self.coords(self.progress_line, self.bar_start_x, self.bar_y, x, self.bar_y)
        self.value = int(((x - self.bar_start_x) / self.bar_length) * 255)
        if self.command: self.command(self.value)

    def get(self): return self.value

class ColorGuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Color Guess Pro")
        self.root.geometry("900x600")
        self.root.configure(bg=COLORS["bg"])
        
        self.player_name = tk.StringVar(value="Hráč1")
        self.scores_file = "scores.json"
        self.game_running = False
        self.image_cache = []
        
        self.header_frame = tk.Frame(self.root, bg=COLORS["panel"], height=65)
        self.content_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.content_frame.pack(fill="both", expand=True)
        self.show_menu()

    def create_circle_img(self, size, color, alpha):
        if not PILLOW_AVAILABLE: return None
        try:
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            draw.ellipse((0, 0, size, size), fill=(r, g, b, alpha))
            return ImageTk.PhotoImage(img)
        except: return None

   
    def load_scores(self):
        if not os.path.exists(self.scores_file): return []
        try:
            with open(self.scores_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

    def save_score(self, name, score):
        data = self.load_scores()
        player_found = False
        for player in data:
            if player['name'] == name:
                if score > player['score']: player['score'] = score
                player_found = True
                break
        if not player_found: data.append({"name": name, "score": score})
        data.sort(key=lambda x: x['score'], reverse=True)
        data = data[:3]
        try:
            with open(self.scores_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        except: pass

   
    def show_menu(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.game_running = False
        self.header_frame.pack_forget()
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        self.image_cache = []
        
        canvas = tk.Canvas(self.content_frame, bg=COLORS["bg"], highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        for _ in range(12):
            size = random.randint(100, 400)
            x, y = random.randint(0, w), random.randint(0, h)
            color = random.choice([COLORS["accent"], COLORS["secondary"]])
            if PILLOW_AVAILABLE:
                img = self.create_circle_img(size, color, 30)
                if img:
                    canvas.create_image(x, y, image=img)
                    self.image_cache.append(img)

        menu_frame = tk.Frame(self.content_frame, bg=COLORS["panel"], padx=40, pady=40)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(menu_frame, text="HÁDEJ BARVU", font=FONT_TITLE, fg="white", bg=COLORS["panel"]).pack(pady=(0, 20))
        tk.Label(menu_frame, text="Tvoje jméno:", font=FONT_BOLD, fg="white", bg=COLORS["panel"]).pack()
        entry = tk.Entry(menu_frame, textvariable=self.player_name, font=("Helvetica", 14), bg=COLORS["bg"], fg="white", insertbackground="white", justify="center", relief="flat")
        entry.pack(pady=10, ipadx=10, ipady=5)
        
        tk.Button(menu_frame, text="ZAČÍT HRU", command=self.start_game, font=FONT_BOLD, bg=COLORS["accent"], fg="white", width=20, pady=10, relief="flat", cursor="hand2").pack(pady=10)
        tk.Button(menu_frame, text="PRAVIDLA", command=self.show_rules, font=FONT_BOLD, bg=COLORS["secondary"], fg="white", width=20, pady=10, relief="flat", cursor="hand2").pack(pady=10)

        lead = tk.Frame(menu_frame, bg=COLORS["panel"])
        lead.pack(fill="x", pady=10)
        tk.Label(lead, text="— ŽEBŘÍČEK —", font=FONT_BOLD, fg=COLORS["secondary"], bg=COLORS["panel"]).pack(pady=5)
        scores = self.load_scores()
        if not scores:
            tk.Label(lead, text="Zatím žádné rekordy", fg="gray", bg=COLORS["panel"]).pack()
        for i, s in enumerate(scores):
            tk.Label(lead, text=f"{i+1}. {s['name']} — {s['score']}", fg="white", bg=COLORS["panel"]).pack()

    def show_rules(self):
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        rules_frame = tk.Frame(self.content_frame, bg=COLORS["panel"], padx=40, pady=40)
        rules_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(rules_frame, text="PRAVIDLA HRY", font=FONT_TITLE, fg="white", bg=COLORS["panel"]).pack(pady=(0, 20))
        rules = [
            "• Zapamatuj si cílovou barvu během 5 sekund.",
            "• Pomocí posuvníků namíchej stejnou barvu.",
            "• Čím přesnější barva, tím více získáš bodů.",
            "• Celkový čas na hru je 120 sekund.",
            "• Dosáhni co nejvyššího skóre!"
        ]
        for rule in rules:
            tk.Label(rules_frame, text=rule, font=FONT_MAIN, fg="white", bg=COLORS["panel"], justify="left").pack(pady=5, anchor="w")
        tk.Button(rules_frame, text="ZAVŘÍT", command=self.show_menu, font=FONT_BOLD, bg=COLORS["accent"], fg="white", padx=30, pady=10, relief="flat", cursor="hand2").pack(pady=20)

   
    def confirm_exit(self):
        """Zobrazí varovné okno před ukončením"""
        self.game_running = False 
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        
        warn_frame = tk.Frame(self.content_frame, bg=COLORS["panel"], padx=40, pady=40)
        warn_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(warn_frame, text="KONEC HRY?", font=FONT_TITLE, fg="white", bg=COLORS["panel"]).pack(pady=10)
        tk.Label(warn_frame, text="Skóre nebude uloženo.\nOpravdu chcete skončit?", font=FONT_MAIN, fg="white", bg=COLORS["panel"]).pack(pady=20)
        
        btn_box = tk.Frame(warn_frame, bg=COLORS["panel"])
        btn_box.pack()
        
        tk.Button(btn_box, text="ZRUŠIT", command=self.resume_game, font=FONT_BOLD, bg=COLORS["secondary"], fg="white", padx=20, pady=10, relief="flat", cursor="hand2").pack(side="left", padx=10)
        tk.Button(btn_box, text="UKONČIT", command=self.show_menu, font=FONT_BOLD, bg=COLORS["accent"], fg="white", padx=20, pady=10, relief="flat", cursor="hand2").pack(side="left", padx=10)

    def resume_game(self):
        self.game_running = True
        self.timer_loop()
        self.guess_phase() 

    def start_game(self):
        self.game_running, self.score, self.remaining_time = True, 0, 120
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        self.header_frame.pack(fill="x", side="top")
        for w_child in self.header_frame.winfo_children(): w_child.destroy()
        
        self.time_lbl = tk.Label(self.header_frame, text="ČAS: 120", font=FONT_BOLD, bg=COLORS["panel"], fg=COLORS["accent"])
        self.time_lbl.pack(side="left", padx=30)
        
        
        tk.Button(self.header_frame, text="ODEJÍT", command=self.confirm_exit, font=FONT_BOLD, bg="#333", fg="white", relief="flat", cursor="hand2").pack(side="right", padx=30)
        
        self.score_lbl = tk.Label(self.header_frame, text="SKÓRE: 0", font=FONT_BOLD, bg=COLORS["panel"], fg=COLORS["secondary"])
        self.score_lbl.pack(side="right", padx=30)
        
        self.timer_loop()
        self.next_round()

    def timer_loop(self):
        if self.game_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_lbl.config(text=f"ČAS: {self.remaining_time}")
            self.root.after(1000, self.timer_loop)
        elif self.game_running and self.remaining_time <= 0:
            self.end_game()

    def next_round(self):
        if not self.game_running: return
        self.target = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        inner = tk.Frame(self.content_frame, bg=COLORS["bg"])
        inner.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(inner, text="ZAPAMATUJ SI", font=FONT_TITLE, fg="white", bg=COLORS["bg"]).pack(pady=10)
        tk.Canvas(inner, width=200, height=200, bg='#%02x%02x%02x' % self.target, highlightthickness=0).pack()
        self.t_val = 5
        self.l_t = tk.Label(inner, text="5", font=FONT_TITLE, fg=COLORS["accent"], bg=COLORS["bg"])
        self.l_t.pack()
        self.wait_mem()

    def wait_mem(self):
        if not self.game_running: return
        if self.t_val > 0:
            self.t_val -= 1
            self.l_t.config(text=str(self.t_val))
            self.root.after(1000, self.wait_mem)
        else: self.guess_phase()

    def guess_phase(self):
        if not self.game_running: return
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        inner = tk.Frame(self.content_frame, bg=COLORS["bg"])
        inner.place(relx=0.5, rely=0.5, anchor="center")
        
        self.sliders = {}
        for c, h in [('Červená', '#FF4444'), ('Zelená', '#44FF44'), ('Modrá', '#4444FF')]:
            s = ModernSlider(inner, c, h, command=self.upd_live)
            s.pack(pady=5); self.sliders[c] = s
            
        self.p_canv = tk.Canvas(inner, width=100, height=100, bg="#000", highlightthickness=0)
        self.p_canv.pack(pady=20)
        tk.Button(inner, text="KONTROLA", command=self.check, bg=COLORS["accent"], fg="white", font=FONT_BOLD, relief="flat", cursor="hand2").pack()

    def upd_live(self, _):
        rgb = (self.sliders['Červená'].get(), self.sliders['Zelená'].get(), self.sliders['Modrá'].get())
        self.p_canv.config(bg='#%02x%02x%02x' % rgb)

    def check(self):
        if not self.game_running: return
        user = (self.sliders['Červená'].get(), self.sliders['Zelená'].get(), self.sliders['Modrá'].get())
        dist = math.sqrt(sum((user[i]-self.target[i])**2 for i in range(3)))
        max_dist = 441.67
        accuracy = max(0, 1 - (dist / max_dist))
        earned = int(100 * (accuracy ** 2))
        if accuracy > 0.99: earned = 100
        self.score += earned
        self.score_lbl.config(text=f"SKÓRE: {self.score}")
        self.res_scr(user, earned, int(accuracy * 100))

    def res_scr(self, user, earned, p):
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        inner = tk.Frame(self.content_frame, bg=COLORS["bg"])
        inner.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(inner, text=f"PŘESNOST: {p}% (+{earned})", font=FONT_TITLE, fg=COLORS["secondary"], bg=COLORS["bg"]).pack()
        box = tk.Frame(inner, bg=COLORS["bg"]); box.pack(pady=20)
        for c, t in [(self.target, "CÍL"), (user, "TY")]:
            f = tk.Frame(box, bg=COLORS["bg"]); f.pack(side="left", padx=20)
            tk.Label(f, text=t, fg="white", bg=COLORS["bg"]).pack()
            tk.Canvas(f, width=100, height=100, bg='#%02x%02x%02x' % c, highlightthickness=0).pack()
        tk.Button(inner, text="DALŠÍ", command=self.next_round, bg=COLORS["accent"], fg="white", font=FONT_BOLD, relief="flat", cursor="hand2").pack()

    def end_game(self):
        self.game_running = False
        self.save_score(self.player_name.get(), self.score)
        self.header_frame.pack_forget()
        for w_child in self.content_frame.winfo_children(): w_child.destroy()
        inner = tk.Frame(self.content_frame, bg=COLORS["bg"])
        inner.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(inner, text="KONEC HRY", font=FONT_TITLE, fg=COLORS["accent"], bg=COLORS["bg"]).pack()
        tk.Label(inner, text=f"SKÓRE: {self.score}", font=FONT_TITLE, fg="white", bg=COLORS["bg"]).pack(pady=20)
        tk.Button(inner, text="DO MENU", command=self.show_menu, font=FONT_BOLD, bg=COLORS["panel"], fg="white", relief="flat", cursor="hand2").pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = ColorGuessGame(root)
    root.mainloop()
