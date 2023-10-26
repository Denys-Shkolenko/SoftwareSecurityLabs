import unittest

from lab1.src.alphabet import Alphabet
from lab1.src.caesar_cipher import CaesarCipher


class TestCaesarCipher(unittest.TestCase):
    def setUp(self):
        """Setup a CaesarCipher instance for testing."""
        self.cipher = CaesarCipher()

    def test_validate_key_valid(self):
        """Test the validate_key method with valid keys."""
        self.assertTrue(self.cipher.validate_key(5))
        self.assertTrue(self.cipher.validate_key(0))
        self.assertTrue(self.cipher.validate_key(len(Alphabet.EN.value) - 1))

    def test_validate_key_invalid(self):
        """Test the validate_key method with invalid keys."""
        self.assertFalse(self.cipher.validate_key(-1))
        self.assertFalse(self.cipher.validate_key(len(Alphabet.EN.value)))
        self.assertFalse(self.cipher.validate_key("A"))  # type: ignore

    def test_cipher(self):
        """Test the cipher method."""
        text = "HELLO"
        expected = "MJQQT"  # Assuming a right shift of 5 for the English alphabet
        self.assertEqual(self.cipher.cipher(text, 5), expected)

    def test_decipher(self):
        """Test the decipher method."""
        text = "MJQQT"
        expected = "HELLO"  # Assuming a right shift of 5 for the English alphabet
        self.assertEqual(self.cipher.decipher(text, 5), expected)

    def test_cipher_with_non_alpha(self):
        """Test the cipher method with non-alphabetical characters."""
        text = "HELLO, WORLD!"
        expected = (
            "MJQQT, bTWQI!"  # Assuming a right shift of 5 for the English alphabet
        )
        self.assertEqual(self.cipher.cipher(text, 5), expected)

    def test_decipher_with_non_alpha(self):
        """Test the decipher method with non-alphabetical characters."""
        text = "MJQQT, bTWQI!"
        expected = (
            "HELLO, WORLD!"  # Assuming a right shift of 5 for the English alphabet
        )
        self.assertEqual(self.cipher.decipher(text, 5), expected)
