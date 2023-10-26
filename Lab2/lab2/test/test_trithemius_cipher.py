import unittest

from lab2.src.alphabet import Alphabet
from lab2.src.trithemius_cipher import Mode, TrithemiusCipher


class TestTrithemiusCipher(unittest.TestCase):
    def setUp(self):
        """Setup a TrithemiusCipher instance for testing."""
        self.cipher = TrithemiusCipher(Alphabet.EN)

    def test_validate_key(self):
        """Test the validate_key method."""
        self.assertTrue(self.cipher.validate_key(Mode.LINEAR, A=2, B=3))
        self.assertFalse(self.cipher.validate_key(Mode.LINEAR, A=2))
        self.assertTrue(self.cipher.validate_key(Mode.NON_LINEAR, A=2, B=3, C=4))
        self.assertFalse(self.cipher.validate_key(Mode.PASSPHRASE))
        self.assertTrue(self.cipher.validate_key(Mode.PASSPHRASE, passphrase="test"))

    def test_cipher_decipher_linear(self):
        """Test encryption and decryption in LINEAR mode."""
        text = "HELLO"
        encrypted = self.cipher.cipher(text, Mode.LINEAR, A=2, B=3)
        decrypted = self.cipher.decipher(encrypted, Mode.LINEAR, A=2, B=3)
        self.assertEqual(text, decrypted)

    def test_cipher_decipher_non_linear(self):
        """Test encryption and decryption in NON_LINEAR mode."""
        text = "HELLO"
        encrypted = self.cipher.cipher(text, Mode.NON_LINEAR, A=2, B=3, C=4)
        decrypted = self.cipher.decipher(encrypted, Mode.NON_LINEAR, A=2, B=3, C=4)
        self.assertEqual(text, decrypted)

    def test_cipher_decipher_passphrase(self):
        """Test encryption and decryption in PASSPHRASE mode."""
        text = "HELLO"
        encrypted = self.cipher.cipher(text, Mode.PASSPHRASE, passphrase="test")
        decrypted = self.cipher.decipher(encrypted, Mode.PASSPHRASE, passphrase="test")
        self.assertEqual(text, decrypted)
