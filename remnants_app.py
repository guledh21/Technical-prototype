import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

DATA_FILE = "remnants.json"
CATEGORIES = ["All", "Sports", "Social", "Restaurant"]
FONT_NAME = "Segoe UI"


class RemnantsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Remnants")
        self.root.geometry("900x540")

        self.remnants = []
        self.visible_indexes = []

        self.filter_var = tk.StringVar(value="All")
        self.category_var = tk.StringVar(value="Sports")

        self.load_data()
        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        main = tk.Frame(self.root, padx=15, pady=15)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 15))

        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(left, text="Map Remnants", font=(
            FONT_NAME, 18, "bold")).pack(anchor="w", pady=(0, 10))
        tk.Label(left, text="Category", font=(
            FONT_NAME, 10, "bold")).pack(anchor="w")

        tk.OptionMenu(left, self.category_var, *
                      CATEGORIES[1:]).pack(anchor="w", fill="x", pady=(0, 10))

        tk.Label(left, text="Place name", font=(
            FONT_NAME, 10, "bold")).pack(anchor="w")
        self.place_entry = tk.Entry(left, width=28, font=(FONT_NAME, 10))
        self.place_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(left, text="Short caption", font=(
            FONT_NAME, 10, "bold")).pack(anchor="w")
        self.caption_text = tk.Text(
            left, width=28, height=6, font=(FONT_NAME, 10), wrap="word")
        self.caption_text.pack(anchor="w", pady=(0, 10))

        tk.Button(left, text="Save remnant", command=self.save_remnant,
                  width=24, font=(FONT_NAME, 10)).pack(anchor="w", pady=(0, 15))
        tk.Button(left, text="Delete selected remnant", command=self.delete_remnant,
                  width=24, font=(FONT_NAME, 10)).pack(anchor="w", pady=(0, 15))

        tk.Label(left, text="Details", font=(
            FONT_NAME, 12, "bold")).pack(anchor="w")
        self.details = tk.Label(
            left,
            text="Select a remnant from the list.",
            font=(FONT_NAME, 10),
            justify="left",
            anchor="w",
            wraplength=250
        )
        self.details.pack(anchor="w", pady=(8, 0))

        top = tk.Frame(right)
        top.pack(fill="x", pady=(0, 10))

        tk.Label(top, text="Filter", font=(
            FONT_NAME, 10, "bold")).pack(side="left")
        tk.OptionMenu(top, self.filter_var, *CATEGORIES,
                      command=lambda _: self.refresh_list()).pack(side="left", padx=10)

        self.listbox = tk.Listbox(right, font=(FONT_NAME, 11))
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.show_details)

    def save_remnant(self):
        place = self.place_entry.get().strip()
        caption = self.caption_text.get("1.0", "end").strip()

        if not place:
            messagebox.showerror("Error", "Enter a place name.")
            return

        if not caption:
            messagebox.showerror("Error", "Enter a caption.")
            return

        remnant = {
            "category": self.category_var.get(),
            "place": place,
            "caption": caption,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.remnants.insert(0, remnant)
        self.save_data()
        self.refresh_list()

        self.place_entry.delete(0, "end")
        self.caption_text.delete("1.0", "end")

    def refresh_list(self):
        self.listbox.delete(0, "end")
        self.visible_indexes = []
        active_filter = self.filter_var.get()

        for i, remnant in enumerate(self.remnants):
            if active_filter != "All" and remnant["category"] != active_filter:
                continue

            self.listbox.insert(
                "end", f"{remnant['category']} | {remnant['place']}")
            self.visible_indexes.append(i)

        self.details.config(text="Select a remnant from the list.")

    def show_details(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return

        remnant = self.remnants[self.visible_indexes[selection[0]]]
        self.details.config(
            text=(
                f"Category: {remnant['category']}\n\n"
                f"Place: {remnant['place']}\n\n"
                f"Caption: {remnant['caption']}\n\n"
                f"Saved: {remnant['created_at']}"
            )
        )

    def delete_remnant(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select a remnant first.")
            return

        del self.remnants[self.visible_indexes[selection[0]]]
        self.save_data()
        self.refresh_list()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    self.remnants = json.load(file)
            except:
                self.remnants = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.remnants, file, indent=4)


root = tk.Tk()
app = RemnantsApp(root)
root.mainloop()
