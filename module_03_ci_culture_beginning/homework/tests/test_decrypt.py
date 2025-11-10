import unittest
from unittest import TestCase

from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    def test_decrypt(self):
        self.assertTrue(decrypt("абра-кадабра.") == "абра-кадабра")
        self.assertTrue(decrypt("абраа..-кадабра") == "абра-кадабра")
        self.assertTrue(decrypt("абраа..-.кадабра") == "абра-кадабра")
        self.assertTrue(decrypt("абра--..кадабра") == "абра-кадабра")
        self.assertTrue(decrypt("абрау...-кадабра") == "абра-кадабра")
        self.assertTrue(decrypt("абра........") == "")
        self.assertTrue(decrypt("абр......a.") == "a")
        self.assertTrue(decrypt("1..2.3") == "23")
        self.assertTrue(decrypt("1.......................") == "")

    def setUp(self):
        self.TESTS: list[tuple[str, str]] = [
            ("абра-кадабра.", "абра-кадабра"),
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
            ('абрау...-кадабра', 'абра-кадабра'),
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1..2.3', '23'),
            ('.', ''),
            ('1.......................', '')
        ]

    def test_decryption(self):
        for i, (encryption, expected) in enumerate(self.TESTS):
            with self.subTest(i=i):
                decryption: str = decrypt(encryption)
                self.assertEqual(decryption, expected)
