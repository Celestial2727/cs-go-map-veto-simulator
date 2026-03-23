import random
import tkinter as tk
from tkinter import messagebox, ttk

# --- MAP DATABASE ---
MAP_CATEGORIES = {
    "Competitive": [
        "Dust2", "Mirage", "Inferno", "Nuke", "Overpass",
        "Vertigo", "Ancient", "Anubis"
    ],
    "Wingman": [
        "Short Dust", "Lake", "Inferno (Wingman)", "Nuke (Wingman)", "Vertigo (Wingman)"
    ],
    "Casual": [
        "Office", "Italy", "Agency", "Cache", "Train"
    ],
    "Custom": []
}

class VetoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CS Veto Simulator V3")
        self.root.geometry("600x700")

        self.mode = tk.StringVar(value="BO1")
        self.category = tk.StringVar(value="Competitive")
        self.maps = []
        self.history = []
        self.stats = {}
        self.turn = "player"

        self.build_ui()
        self.load_maps()

    # --- UI ---
    def build_ui(self):
        top = tk.Frame(self.root)
        top.pack(pady=10)

        ttk.Label(top, text="Mode:").pack(side=tk.LEFT)
        ttk.Combobox(top, textvariable=self.mode, values=["BO1", "BO3"], width=5).pack(side=tk.LEFT, padx=5)

        ttk.Label(top, text="Category:").pack(side=tk.LEFT)
        ttk.Combobox(top, textvariable=self.category,
                     values=list(MAP_CATEGORIES.keys()), width=12,
                     state="readonly").pack(side=tk.LEFT, padx=5)

        ttk.Button(top, text="Load", command=self.load_maps).pack(side=tk.LEFT, padx=5)

        # Custom map entry
        custom_frame = tk.Frame(self.root)
        custom_frame.pack(pady=5)
        self.custom_entry = ttk.Entry(custom_frame, width=30)
        self.custom_entry.pack(side=tk.LEFT)
        ttk.Button(custom_frame, text="Add Custom Map", command=self.add_custom_map).pack(side=tk.LEFT, padx=5)

        # Map buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Info
        self.label = ttk.Label(self.root, text="Your turn: Ban a map", font=("Arial", 12))
        self.label.pack(pady=5)

        # History
        self.history_box = tk.Text(self.root, height=10, width=60)
        self.history_box.pack(pady=5)

        # Stats
        self.stats_label = ttk.Label(self.root, text="Stats: ")
        self.stats_label.pack(pady=5)

        # Reset
        ttk.Button(self.root, text="Reset", command=self.reset).pack(pady=10)

    # --- LOGIC ---
    def load_maps(self):
        self.maps = MAP_CATEGORIES[self.category.get()].copy()
        self.history.clear()
        self.turn = "player"
        self.update_buttons()
        self.update_history()
        self.label.config(text="Your turn: Ban a map")

    def add_custom_map(self):
        name = self.custom_entry.get().strip()
        if name:
            MAP_CATEGORIES["Custom"].append(name)
            self.custom_entry.delete(0, tk.END)

    def update_buttons(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for m in self.maps:
            ttk.Button(self.frame, text=m, width=25,
                       command=lambda map_name=m: self.player_action(map_name)).pack(pady=2)

    def update_history(self):
        self.history_box.delete(1.0, tk.END)
        for h in self.history:
            self.history_box.insert(tk.END, h + "\n")

    def update_stats(self, selected_maps):
        for m in selected_maps:
            self.stats[m] = self.stats.get(m, 0) + 1

        total = sum(self.stats.values())
        text = "Stats:\n"
        for m, count in self.stats.items():
            pct = (count / total) * 100 if total else 0
            text += f"{m}: {pct:.1f}%\n"
        self.stats_label.config(text=text)

    def player_action(self, map_name):
        if self.turn != "player": return

        self.maps.remove(map_name)
        self.history.append(f"You banned: {map_name}")
        self.update_history()

        if self.check_end(): return

        self.turn = "ai"
        self.label.config(text="AI thinking...")
        self.root.after(700, self.ai_action)
        self.update_buttons()

    def ai_action(self):
        choice = random.choice(self.maps)
        self.maps.remove(choice)
        self.history.append(f"AI banned: {choice}")
        self.update_history()

        if self.check_end(): return

        self.turn = "player"
        self.label.config(text="Your turn: Ban a map")
        self.update_buttons()

    def check_end(self):
        if self.mode.get() == "BO1" and len(self.maps) == 1:
            self.end_game(self.maps)
            return True
        if self.mode.get() == "BO3" and len(self.maps) == 3:
            self.end_game(self.maps)
            return True
        return False

    def end_game(self, maps):
        self.update_stats(maps)
        messagebox.showinfo("Result", "Maps selected:\n" + "\n".join(maps))

    def reset(self):
        self.load_maps()


if __name__ == "__main__":
    root = tk.Tk()
    app = VetoApp(root)
    root.mainloop()