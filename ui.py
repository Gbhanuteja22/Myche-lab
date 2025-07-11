# ui.py
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from chemistry import elements
from ai_engine import ask_gemini
import re
from PIL import Image, ImageTk
import os

class VirtualLabApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI-Powered Virtual Chemistry Lab")
        self.root.geometry("1400x800")

        # Left area with only Beaker
        self.left_frame = tk.Frame(self.root, width=200, bg='white')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(self.left_frame, bg='white', width=200)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.center_frame = tk.Frame(self.root, bg='white', width=500)
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.root, width=280, bg='lightgrey')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.lab_items = {}
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.selected_elements = []
        self.element_texts = []
        self.element_weights = {}

        self.predicted_image_label = None

        self.load_beaker_only()
        self.build_periodic_table()
        self.build_prediction_output()

    def load_beaker_only(self):
        name = "beaker"
        x, y = 50, 200
        rect = self.canvas.create_rectangle(x, y, x+100, y+100, fill="lightblue", tags=("draggable", name))
        text = self.canvas.create_text(x+50, y+50, text=name.title(), tags="draggable")
        self.lab_items[name] = rect

        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.on_drop)

    def build_periodic_table(self):
        tk.Label(self.sidebar, text="Periodic Table", bg="lightgrey", font=("Arial", 14, "bold")).pack(pady=15)

        self.element_listbox = tk.Listbox(self.sidebar, selectmode=tk.MULTIPLE, width=25)
        for symbol, data in elements.items():
            self.element_listbox.insert(tk.END, f"{symbol} - {data['name']}")
        self.element_listbox.pack(pady=10)

        spacing = 10
        tk.Button(self.sidebar, text="Add to Beaker", command=self.add_elements_to_beaker).pack(pady=spacing)
        tk.Button(self.sidebar, text="Predict Compound", command=self.predict_compound).pack(pady=spacing)
        tk.Button(self.sidebar, text="Clear Beaker", command=self.clear_beaker).pack(pady=spacing)
        tk.Button(self.sidebar, text="Reset Elements", command=self.reset_elements).pack(pady=spacing)
        tk.Button(self.sidebar, text="Export Prediction", command=self.export_result).pack(pady=spacing)

        self.selected_label = tk.Label(self.sidebar, text="Selected: None", bg="lightgrey", wraplength=260, justify=tk.LEFT)
        self.selected_label.pack(pady=15)

    def build_prediction_output(self):
        tk.Label(self.center_frame, text="Prediction Output", bg="white", font=("Arial", 14, "bold")).pack(pady=15)
        self.prediction_output = tk.Text(self.center_frame, wrap=tk.WORD, height=20, width=60)
        self.prediction_output.pack(padx=10, pady=10)

        self.predicted_image_label = tk.Label(self.center_frame, bg="white")
        self.predicted_image_label.pack(pady=10)

    def add_elements_to_beaker(self):
        selected_indices = self.element_listbox.curselection()
        new_elements = [self.element_listbox.get(i).split(' - ')[0] for i in selected_indices]

        for sym in new_elements:
            count = simpledialog.askinteger("Atom Count", f"How many atoms of {sym}?", minvalue=1, initialvalue=1)
            weight = simpledialog.askfloat("Optional: Weight", f"Weight for {sym}? (g, optional)", minvalue=0.0)
            self.element_weights[sym] = {"count": count, "weight": weight if weight else None}

        self.selected_elements = list(self.element_weights.keys())
        self.update_beaker_display()

    def update_beaker_display(self):
        for text_id in self.element_texts:
            self.canvas.delete(text_id)
        self.element_texts.clear()

        beaker_coords = self.canvas.coords(self.lab_items.get("beaker", (100, 100, 200, 200)))
        x = (beaker_coords[0] + beaker_coords[2]) / 2
        y = beaker_coords[3] - 20

        display_lines = []

        for i, sym in enumerate(self.selected_elements):
            data = self.element_weights[sym]
            text = f"{sym} x{data['count']}"
            if data['weight']:
                text += f" ({data['weight']}g)"
            display_lines.append(text)
            text_id = self.canvas.create_text(x, y - i * 20, text=text, fill="black", font=("Arial", 12))
            self.element_texts.append(text_id)

        self.selected_label.config(text="Selected:\n" + "\n".join(display_lines))

    def clean_text(self, text):
        text = re.sub(r'[\*#`|]', '', text)
        text = re.sub(r'\n{2,}', '\n', text)
        return text.strip()

    def predict_compound(self):
        if not self.selected_elements:
            self.prediction_output.delete(1.0, tk.END)
            self.prediction_output.insert(tk.END, "Please add elements first.")
            return

        prompt = "Given the following elements and their details:\n"
        for sym in self.selected_elements:
            data = self.element_weights[sym]
            line = f"{sym} ({elements[sym]['name']}): {data['count']} atoms"
            if data['weight']:
                line += f", {data['weight']}g"
            prompt += f"- {line}\n"

        prompt += (
            "\nPredict the resulting compound (if any) and return only:\n"
            "- Chemical formula\n"
            "- Color\n"
            "- Other name or original name\n"
            "- Reaction\n"
            "- Properties (max 5 points)\n"
            "No tables or markdown formatting. Plain text only."
        )

        try:
            result = ask_gemini(prompt)
            clean = self.clean_text(result)
            self.prediction_output.delete(1.0, tk.END)
            self.prediction_output.insert(tk.END, clean)
            self.update_image_if_available(clean)
        except Exception as e:
            self.prediction_output.delete(1.0, tk.END)
            self.prediction_output.insert(tk.END, f"Error: {e}")

    def update_image_if_available(self, text):
        keyword = "glucose" if "C6H12O6" in text or "dextrose" in text.lower() else None
        image_map = {
            "glucose": "glucose.png"
        }
        if keyword and os.path.exists(image_map[keyword]):
            img = Image.open(image_map[keyword])
            img = img.resize((200, 200))
            tk_img = ImageTk.PhotoImage(img)
            self.predicted_image_label.config(image=tk_img)
            self.predicted_image_label.image = tk_img
        else:
            self.predicted_image_label.config(image=None)
            self.predicted_image_label.image = None

    def export_result(self):
        result = self.prediction_output.get(1.0, tk.END).strip()
        if not result:
            messagebox.showerror("Error", "Nothing to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(result)
            messagebox.showinfo("Success", f"Saved to {path}")

    def clear_beaker(self):
        for text_id in self.element_texts:
            self.canvas.delete(text_id)
        self.element_texts.clear()
        self.selected_elements = []
        self.element_weights.clear()
        self.selected_label.config(text="Selected: None")
        self.predicted_image_label.config(image=None)
        self.predicted_image_label.image = None

    def reset_elements(self):
        self.element_listbox.selection_clear(0, tk.END)
        self.clear_beaker()
        self.prediction_output.delete(1.0, tk.END)

    def on_start(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = item
        coords = self.canvas.coords(item)
        self.drag_data["x"] = event.x - coords[0]
        self.drag_data["y"] = event.y - coords[1]

    def on_drag(self, event):
        item = self.drag_data["item"]
        if item:
            new_x = event.x - self.drag_data["x"]
            new_y = event.y - self.drag_data["y"]
            coords = self.canvas.coords(item)
            width = coords[2] - coords[0]
            height = coords[3] - coords[1]
            self.canvas.coords(item, new_x, new_y, new_x + width, new_y + height)

    def on_drop(self, event):
        self.drag_data["item"] = None

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VirtualLabApp()
    app.run()
