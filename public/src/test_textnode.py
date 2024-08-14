import unittest
from urllib.parse import urlparse
from textnode import TextNode
from Enums import TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node1 = TextNode("This is a TextNode", TextType.BOLD, "https://www.weather.com")
        text_node2 = TextNode("This is a TextNode", TextType.BOLD, "https://www.weather.com")
        self.assertEqual(text_node1, text_node2)

    def test_inequiv(self):
        text_node1 = TextNode("This is TextNode1", TextType.BOLD, "https://www.weather.com")
        text_node2 = TextNode("This is TextNode2", TextType.BOLD, "https://www.weather.com")
        self.assertNotEqual(text_node1, text_node2)

    def test_inequiv2(self):
        text_node1 = TextNode("This is TextNode1", TextType.BOLD, "https://www.weather.com")
        text_node2 = TextNode("This is TextNode1", TextType.CODE, "https://www.weather.com")
        self.assertNotEqual(text_node1, text_node2)

    def test_URL(self):
        text_node1 = TextNode("This is TextNode1", TextType.BOLD, "https://www.weather.com")
        result = urlparse(text_node1.url)
        self.assertTrue(all([result.scheme, result.netloc]))
    
    def test_repr(self):
        text_node1 = TextNode("This is TextNode1", TextType.BOLD, "https://www.weather.com")
        self.assertEqual(repr(text_node1), f"TextNode(This is TextNode1, {TextType.BOLD}, https://www.weather.com)")

if __name__ == "__main__":
    unittest.main()