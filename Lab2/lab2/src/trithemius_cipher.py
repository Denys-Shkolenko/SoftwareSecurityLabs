from lab2.src.alphabet import Alphabet
from lab2.src.mode import Mode


class TrithemiusCipher:
    """
    Implementation of the Trithemius Cipher.

    Attributes:
        alphabet (str): The alphabet set used for encryption and decryption.

    Methods:
        validate_key: Validates the given keys based on the mode.
        cipher: Encrypts the given text using the Trithemius Cipher.
        decipher: Decrypts the given text using the Trithemius Cipher.
    """

    def __init__(self, alphabet: Alphabet):
        """
        Initializes the TrithemiusCipher with a given alphabet.

        Args:
            alphabet (Alphabet): The alphabet set used for encryption and decryption.
        """
        self.alphabet = alphabet.value

    @staticmethod
    def validate_key(mode: Mode, **kwargs) -> bool:
        """
        Validates the keys based on the mode.

        Args:
            mode (Mode): The mode of the cipher.
            **kwargs: Key arguments for the corresponding mode.

        Returns:
            bool: True if the key(s) are valid, False otherwise.
        """
        if mode == Mode.LINEAR:
            return "A" in kwargs and "B" in kwargs
        elif mode == Mode.NON_LINEAR:
            return "A" in kwargs and "B" in kwargs and "C" in kwargs
        elif mode == Mode.PASSPHRASE:
            return "passphrase" in kwargs and len(kwargs["passphrase"]) > 0
        return False

    def _calculate_k(self, mode: Mode, p: int, **kwargs) -> int:
        """
        Calculates the value of 'k' based on the mode and position.

        Args:
            mode (Mode): The mode of the cipher.
            p (int): The position of the character in the message.
            **kwargs: Key arguments for the corresponding mode.

        Returns:
            int: The calculated value of 'k'.
        """
        if mode == Mode.LINEAR:
            return kwargs["A"] * p + kwargs["B"]
        elif mode == Mode.NON_LINEAR:
            return kwargs["A"] ** 2 + kwargs["B"] * p + kwargs["C"]
        elif mode == Mode.PASSPHRASE:
            char_position = self.alphabet.index(
                kwargs["passphrase"][p % len(kwargs["passphrase"])]
            )
            return char_position
        return 0

    def cipher(self, text: str, mode: Mode, **kwargs) -> str:
        """
        Encrypts the given text using the Trithemius Cipher.

        Args:
            text (str): The text to be encrypted.
            mode (Mode): The mode of the cipher.
            **kwargs: Key arguments for the corresponding mode.

        Returns:
            str: The encrypted text.
        """
        encrypted_text = ""
        n = len(self.alphabet)

        for idx, char in enumerate(text):
            if char in self.alphabet:
                x = self.alphabet.index(char)
                k = self._calculate_k(mode, idx, **kwargs)
                y = (x + k) % n
                encrypted_text += self.alphabet[y]
            else:
                encrypted_text += char

        return encrypted_text

    def decipher(self, text: str, mode: Mode, **kwargs) -> str:
        """
        Decrypts the given text using the Trithemius Cipher.

        Args:
            text (str): The text to be decrypted.
            mode (Mode): The mode of the cipher.
            **kwargs: Key arguments for the corresponding mode.

        Returns:
            str: The decrypted text.
        """
        decrypted_text = ""
        n = len(self.alphabet)

        for idx, char in enumerate(text):
            if char in self.alphabet:
                y = self.alphabet.index(char)
                k = self._calculate_k(mode, idx, **kwargs)
                x = (y + n - (k % n)) % n
                decrypted_text += self.alphabet[x]
            else:
                decrypted_text += char

        return decrypted_text
