import tkinter as tk

from lab1.src.caesar_app import CaesarApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarApp(root)
    root.mainloop()
