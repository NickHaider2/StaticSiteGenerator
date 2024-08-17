import unittest
from urllib.parse import urlparse
from textnode import TextNode
from textnode import text_node_to_html_node
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

class TestTextNodetoHTML(unittest.TestCase):
    def test_text_to_html_node_Bold(self):
        text_node1 = text_node_to_html_node(TextNode("This is TextNode1", TextType.BOLD, "https://www.weather.com"))
        self.assertEqual(text_node1.tag, "b")
        self.assertEqual(text_node1.value, "This is TextNode1")

    def test_text_to_html_node_Link(self):
        text_node2 = text_node_to_html_node(TextNode("This is a Link", TextType.LINK, "https://www.weather.com"))
        self.assertEqual(text_node2.tag, "a")
        self.assertEqual(text_node2.props, {"href":  "https://www.weather.com"})

    def test_text_to_html_node_Image(self):
        text_node3 = text_node_to_html_node(TextNode("This is an Image", TextType.IMAGE, "https://www.reddit.com"))
        self.assertEqual(text_node3.tag, "img")
        self.assertEqual(text_node3.props, {"src": "https://www.reddit.com", "alt": "This is an Image"})


if __name__ == "__main__":
    unittest.main()