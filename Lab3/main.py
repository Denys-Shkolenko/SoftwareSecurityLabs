from typing import List, Tuple, Dict, Optional


class VerseKey:
    """Class to process the verse and create a key table for ciphering."""

    def __init__(self, verse: str, size: int = 10):
        self.verse = verse
        self.size = size
        self.key_table = self._create_key_table()

    def _create_key_table(self) -> Dict[str, List[Tuple[int, int]]]:
        """Create a key table mapping each character to its positions."""
        table = {}
        words = self.verse.split()
        for row, word in enumerate(words[:self.size]):
            for col, char in enumerate(word[:self.size]):
                if char not in table:
                    table[char] = []
                table[char].append((row + 1, col + 1))
        return table

    def get_char_positions(self, char: str) -> Optional[List[Tuple[int, int]]]:
        """Return positions of a character in the key table."""
        return self.key_table.get(char)


class VerseCipher:
    """Class for encrypting and decrypting messages using a verse as key."""

    def __init__(self, verse_key: VerseKey):
        self.verse_key = verse_key

    def encrypt(self, message: str) -> str:
        """Encrypt a message using the verse key."""
        encrypted = []
        for char in message:
            positions = self.verse_key.get_char_positions(char)
            if positions:
                # Choose a random position for each character
                encrypted.append(f"{positions[0][0]}/{positions[0][1]}")
            else:
                encrypted.append(f"{char}")
        return ', '.join(encrypted)

    def decrypt(self, cipher_text: str) -> str:
        """Decrypt a cipher text using the verse key."""
        decrypted = []
        for part in cipher_text.split(', '):
            if '/' in part:
                row, col = map(int, part.split('/'))
                for char, positions in self.verse_key.key_table.items():
                    if (row, col) in positions:
                        decrypted.append(char)
                        break
            else:
                decrypted.append(part)
        return ''.join(decrypted)


# Example Usage
verse = "Your chosen verse here"
key = VerseKey(verse)
cipher = VerseCipher(key)

encrypted_message = cipher.encrypt("Your message here")
print("Encrypted:", encrypted_message)

decrypted_message = cipher.decrypt(encrypted_message)
print("Decrypted:", decrypted_message)
