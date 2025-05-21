from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog

WIDTH = 800
HEIGHT = 600
def main():
    root = Tk()
    root.geometry("800x600")
    root.title("Farfisa")
    root.resizable(True, True)

    btn = Button(root, text = "open image", command = open_img(root)).grid(row = 1, columnspan = 3)

    root.mainloop()
def open_img(root):
    file = openfilename()

    img = Image.open(file)

    img = img.resize((int(WIDTH*0.5), int(HEIGHT*0.5)), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    panel = Label(root, image=img)
    panel.image = img
    panel.grid(row = 2)



def openfilename():
    filename = filedialog.askopenfilename(title='Open')
    return filename

if __name__ == "__main__":
    main()


