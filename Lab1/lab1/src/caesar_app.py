import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from lab1.src.alphabet import Alphabet
from lab1.src.caesar_cipher import CaesarCipher


class CaesarApp:
    """A class to manage the Caesar Cipher GUI application.

    Attributes:
        root (tk.Tk): The root window for the application.
        cipher (CaesarCipher): Instance of CaesarCipher for encryption/decryption operations.
        menu (tk.Menu): Menu bar for the application.
        file_menu (tk.Menu): File submenu in the menu bar.
        cipher_menu (tk.Menu): Cipher submenu in the menu bar.
        text (tk.Text): Text widget for user to input and view text.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the application with a given root window.

        Args:
            root (tk.Tk): The root window for the application.
        """
        self.root = root
        self.cipher: CaesarCipher | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.root.title("Caesar Cipher")
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu setup
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open...", command=self._open_file)
        self.file_menu.add_command(label="Save...", command=self._save_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Cipher menu setup
        self.cipher_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Cipher", menu=self.cipher_menu)
        self.cipher_menu.add_command(label="Encrypt", command=self._encrypt_text)
        self.cipher_menu.add_command(label="Decrypt", command=self._decrypt_text)

        # Text widget setup
        self.text = tk.Text(self.root, wrap=tk.WORD)
        self.text.pack(expand=True, fill=tk.BOTH)

        # Info menu setup
        self.info_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Info", menu=self.info_menu)
        self.info_menu.add_command(label="About", command=self._show_info)

    def _show_info(self) -> None:
        """
        Display developer's information.
        """
        messagebox.showinfo(
            "About", "Developer: Denys Shkolenko <denys.shkolenko@gmail.com>"
        )

    def _open_file(self) -> None:
        """
        Open a file and load its content into the text widget.
        """
        file_path = filedialog.askopenfilename()
        with open(file_path, "r", encoding="utf-8") as file:
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.INSERT, file.read())

    def _save_file(self) -> None:
        """
        Save the content of the text widget to a file.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.text.get(1.0, tk.END))

    def _encrypt_text(self) -> None:
        """
        Encrypt the content of the text widget using the Caesar Cipher.
        """
        key = simpledialog.askinteger("Key", "Enter key (integer):")
        if key is not None:
            language = (
                Alphabet.UK
                if messagebox.askyesno("Language", "Use Ukrainian language?")
                else Alphabet.EN
            )
            self.cipher = CaesarCipher(language)
            encrypted = self.cipher.cipher(self.text.get(1.0, tk.END), key)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.INSERT, encrypted)

    def _decrypt_text(self) -> None:
        """
        Decrypt the content of the text widget using the Caesar Cipher.
        """
        key = simpledialog.askinteger("Key", "Enter key (integer):")
        if key is not None:
            language = (
                Alphabet.UK
                if messagebox.askyesno("Language", "Use Ukrainian language?")
                else Alphabet.EN
            )
            self.cipher = CaesarCipher(language)
            decrypted = self.cipher.decipher(self.text.get(1.0, tk.END), key)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.INSERT, decrypted)
