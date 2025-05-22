import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from tkinter import filedialog, messagebox
import json
import os
# GUI for Farfisa
class ImageObserver:
    def __init__(self, master):
        self.master = master
        self.master.title("Farfisa")

        self.image_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All Files", "*.*")),
        )
        if not self.image_paths:
            messagebox.showerror("Error", "No images selected.")
            self.master.quit()
            return

        self.index = 0
        self.is_animated = False
        self.frames = []
        self.delay = 100

        self.label = tk.Label(master)
        self.label.pack(padx=10, pady=10)

        btn_frame = tk.Frame(self.master)
        btn_frame.pack()

        prev_button = tk.Button(btn_frame, text=" << Previous", command=self.show_previous_image)
        prev_button.grid(row=0, column=0, padx=5)

        next_button = tk.Button(btn_frame, text="Next >>", command=self.show_next_image)
        next_button.grid(row=0, column=1, padx=5)

        json_button = tk.Button(btn_frame, text="Load JSON", command=self.open_json_window)
        json_button.grid(row=0, column=2, padx=5)

        input_btn = tk.Button(btn_frame, text="Chat", command=self.open_input_window)
        input_btn.grid(row=0, column=3, padx=5)

        self.photo = None
        self.show_image()

    def show_image(self):
        self.is_animated = False
        path = self.image_paths[self.index]

        if path.lower().endswith(".gif"):
            img = Image.open(path)
            self.frames = [ImageTk.PhotoImage(frame.copy().resize((600, 400), Image.Resampling.LANCZOS))
                           for frame in ImageSequence.Iterator(img)]
            self.delay = img.info.get("duration", 100)
            self.is_animated = True
            self.animate(0)
        else:
            img = Image.open(path)
            img = img.resize((600, 400), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.label.config(image=self.photo)

        self.master.title (f"Farfisa - {self.index + 1}/{len(self.image_paths)}")

    def animate(self, frame_index):
        if not self.is_animated:
            return
        self.label.config(image=self.frames[frame_index])
        next_index = (frame_index + 1) % len(self.image_paths)
        self.master.after(self.delay, lambda: self.animate(next_index))

    def show_next_image(self):
        if self.index < len(self.image_paths) - 1:
            self.index += 1
            self.show_image()
        else:
            messagebox.showerror("Error", "This is the last image.")

    def show_previous_image(self):
        if self.index > 0:
            self.index -= 1
            self.show_image()
        else:
            messagebox.showerror("Error", "This is the first image.")

    def open_json_window(self):
        path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")),
        )
        if not path:
            return
        try:
            with open(path, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")
            return

        win = tk.Toplevel(self.master)
        win.title(f"Json Viewer - {os.path.basename(path)}")

        text = tk.Text(win, wrap='none')
        text.pack(fill='both', expand=True)
        xscroll = tk.Scrollbar(win, orient='horizontal', command=text.xview)
        yscroll = tk.Scrollbar(win, orient='vertical', command=text.yview)
        xscroll.pack(side='bottom', fill='x')
        yscroll.pack(side='right', fill='y')
        text.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        text.insert('1.0', pretty)
        text.config(state='disabled')


    def open_input_window(self):
        win = tk.Toplevel(self.master)
        win.title("Chat With Me")
        tk.Label(win, text="Message:").pack(padx=10, pady=(10,0))
        entry = tk.Entry(win, width=50)
        entry.pack(padx=10, pady=5)
        entry.focus_set()

        def send_message(event=None):
            message = entry.get().strip()
            if not message:
                messagebox.showerror("Empty", "Please enter a message.")
                return
            win.destroy()
            self.show_message_window(message)

        entry.bind('<Return>', send_message)
        send_btn = tk.Button(win, text="Send", command=send_message)
        send_btn.pack(pady=(0, 10))


    def show_message_window(self, message):
        win = tk.Toplevel(self.master)
        win.title("Your message: ")
        tk.Label(win, text=message, wraplength=400, justify='left').pack(padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageObserver(root)
    root.mainloop()