from lab1.src.alphabet import Alphabet


class CaesarCipher:
    """
    A class to perform Caesar Cipher encryption and decryption.

    Attributes:
        alphabet (Alphabet): The language's alphabet used for the cipher.
    """

    def __init__(self, alphabet: Alphabet = Alphabet.EN) -> None:
        """
        Initialize the cipher with a specific language's alphabet.

        Args:
            alphabet (Alphabet): The language's alphabet to be used. Defaults to English.
        """
        self.alphabet = alphabet

    def validate_key(self, key: int) -> bool:
        """
        Check if the given key is valid for the cipher.

        Args:
            key (int): The key to validate.

        Returns:
            bool: True if the key is valid, False otherwise.
        """
        return isinstance(key, int) and 0 <= key < len(self.alphabet.value)

    def cipher(self, text: str, key: int) -> str:
        """
        Encrypt the given text using the Caesar Cipher.

        Args:
            text (str): The text to be encrypted.
            key (int): The encryption key.

        Returns:
            str: The encrypted text.

        Raises:
            ValueError: If the key is invalid.
        """
        if not self.validate_key(key):
            raise ValueError("Invalid key")
        return self._shift(text, key)

    def decipher(self, text: str, key: int) -> str:
        """
        Decrypt the given text using the Caesar Cipher.

        Args:
            text (str): The text to be decrypted.
            key (int): The decryption key.

        Returns:
            str: The decrypted text.
        """
        return self._shift(text, -key)

    def _shift(self, text: str, key: int) -> str:
        """
        Internal method to shift the characters in the text by the given key.

        Args:
            text (str): The text to be shifted.
            key (int): The shift key.

        Returns:
            str: The shifted text.
        """
        shifted_text = ""
        for char in text:
            if char in self.alphabet.value:
                char_index = (self.alphabet.value.index(char) + key) % len(
                    self.alphabet.value
                )
                shifted_text += self.alphabet.value[char_index]
            else:
                shifted_text += char
        return shifted_text
