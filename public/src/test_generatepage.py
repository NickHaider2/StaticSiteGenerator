import unittest
from generatepage import extract_title

class TestGeneratePage(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# This is a title.\n\nThis is a paragraph."
        self.assertEqual(extract_title(markdown),"This is a title.")

    def test_extract_no_title(self):
        markdown = "This is a paragraph."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_no_h1(self):
        markdown = "### Some random title.\n\nThis is a paragraph."
        with self.assertRaises(ValueError):
            extract_title(markdown)

