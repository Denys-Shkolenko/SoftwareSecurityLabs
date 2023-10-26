import tkinter as tk
from tkinter import filedialog, messagebox

from lab2.src.alphabet import Alphabet
from lab2.src.mode import Mode
from lab2.src.trithemius_cipher import TrithemiusCipher


class TrithemiusApp:
    """A class to manage the Trithemius Cipher GUI application.

    Attributes:
        root (tk.Tk): The root window for the application.
        cipher (TrithemiusCipher): Instance of TrithemiusCipher for encryption/decryption operations.
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
        self.cipher: TrithemiusCipher | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.root.title("Trithemius Cipher")
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

    @staticmethod
    def _show_info() -> None:
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

    @staticmethod
    def _get_mode_inputs(mode: Mode) -> dict:
        """
        Get the required inputs for a given mode.

        Args:
            mode (Mode): The selected mode.

        Returns:
            dict: A dictionary of inputs for the mode.
        """
        inputs: dict[str, int | str | None] = {}

        # Create input dialog
        input_dialog = tk.Toplevel()
        input_dialog.title("Enter Parameters")
        input_dialog.geometry("250x300")
        input_dialog.resizable(False, False)

        if mode in [Mode.LINEAR, Mode.NON_LINEAR]:
            tk.Label(input_dialog, text="Enter A (integer):").pack(pady=5)
            a_entry = tk.Entry(input_dialog)
            a_entry.pack(pady=5)

            tk.Label(input_dialog, text="Enter B (integer):").pack(pady=5)
            b_entry = tk.Entry(input_dialog)
            b_entry.pack(pady=5)

        if mode == Mode.NON_LINEAR:
            tk.Label(input_dialog, text="Enter C (integer):").pack(pady=5)
            c_entry = tk.Entry(input_dialog)
            c_entry.pack(pady=5)

        if mode == Mode.PASSPHRASE:
            tk.Label(input_dialog, text="Enter passphrase:").pack(pady=5)
            passphrase_entry = tk.Entry(input_dialog, show="*")
            passphrase_entry.pack(pady=5)

        def on_confirm():
            if mode in [Mode.LINEAR, Mode.NON_LINEAR]:
                inputs["A"] = int(a_entry.get())
                inputs["B"] = int(b_entry.get())
            if mode == Mode.NON_LINEAR:
                inputs["C"] = int(c_entry.get())
            if mode == Mode.PASSPHRASE:
                inputs["passphrase"] = passphrase_entry.get()
            input_dialog.destroy()

        tk.Button(input_dialog, text="Confirm", command=on_confirm).pack(pady=10)
        input_dialog.transient()
        input_dialog.grab_set()
        input_dialog.wait_window()

        return inputs

    def _choose_mode_via_radiobuttons(self) -> Mode:
        """Create a dialog with radio buttons to choose encryption/decryption mode."""

        mode_dialog = tk.Toplevel(self.root)
        mode_dialog.title("Choose Mode")
        mode_dialog.geometry("300x150")
        mode_dialog.resizable(False, False)

        mode_var = tk.StringVar(value="LINEAR")  # Default value

        modes = [
            ("Linear", Mode.LINEAR),
            ("Non-Linear", Mode.NON_LINEAR),
            ("Passphrase", Mode.PASSPHRASE),
        ]

        for text, mode in modes:
            tk.Radiobutton(
                mode_dialog, text=text, variable=mode_var, value=mode.name
            ).pack(anchor=tk.W)

        def on_confirm():
            mode_dialog.selected_mode = Mode(mode_var.get())
            mode_dialog.destroy()

        tk.Button(mode_dialog, text="Confirm", command=on_confirm).pack(pady=10)
        mode_dialog.transient(self.root)
        mode_dialog.grab_set()
        mode_dialog.wait_window()

        return getattr(mode_dialog, "selected_mode", Mode.LINEAR)

    def _encrypt_text(self) -> None:
        """
        Encrypt the content of the text widget using the Trithemius Cipher.
        """
        selected_mode = self._choose_mode_via_radiobuttons()
        inputs = None

        if selected_mode is not None:
            inputs = self._get_mode_inputs(selected_mode)
            if not TrithemiusCipher.validate_key(selected_mode, **inputs):
                messagebox.showerror("Error", "Invalid Key Inputs!")
                return

        if inputs is not None:
            language = (
                Alphabet.UK
                if messagebox.askyesno("Language", "Use Ukrainian language?")
                else Alphabet.EN
            )
            self.cipher = TrithemiusCipher(language)
            encrypted = self.cipher.cipher(
                self.text.get(1.0, tk.END), selected_mode, **inputs
            )
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.INSERT, encrypted)

    def _decrypt_text(self) -> None:
        """
        Decrypt the content of the text widget using the Trithemius Cipher.
        """
        selected_mode = self._choose_mode_via_radiobuttons()
        inputs = None

        if selected_mode is not None:
            inputs = self._get_mode_inputs(selected_mode)
            if not TrithemiusCipher.validate_key(selected_mode, **inputs):
                messagebox.showerror("Error", "Invalid Key Inputs!")
                return

        if inputs is not None:
            language = (
                Alphabet.UK
                if messagebox.askyesno("Language", "Use Ukrainian language?")
                else Alphabet.EN
            )
            self.cipher = TrithemiusCipher(language)
            decrypted = self.cipher.decipher(
                self.text.get(1.0, tk.END), selected_mode, **inputs
            )
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.INSERT, decrypted)
