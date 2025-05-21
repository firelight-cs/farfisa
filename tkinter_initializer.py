import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from tkinter import filedialog, messagebox

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


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageObserver(root)
    root.mainloop()