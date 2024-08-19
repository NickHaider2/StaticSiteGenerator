import unittest
from textnode import TextNode
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    convert_text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)
from Enums import TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_only_bold_delimiter_split(self):
        nodes_to_split = [
            TextNode("This is text with a `code block` word.", TextType.CODE),
            TextNode("Another line of text with some **Bold Words**",
                     TextType.BOLD),
            TextNode("*Italic* Example Block", TextType.ITALIC),
            TextNode("Checking for bold where there is none", TextType.BOLD),
            TextNode("Just some regular text", TextType.TEXT)]

        bold_splits = split_nodes_delimiter(
            nodes_to_split, "**", TextType.BOLD)

        self.assertListEqual(bold_splits,
                             [
                                 TextNode("This is text with a `code block` word.",
                                          TextType.CODE),
                                 TextNode(
                                     "Another line of text with some ", TextType.TEXT),
                                 TextNode("Bold Words", TextType.BOLD),
                                 TextNode("*Italic* Example Block",
                                          TextType.ITALIC),
                                 TextNode(
                                     "Checking for bold where there is none", TextType.TEXT),
                                 TextNode("Just some regular text",
                                          TextType.TEXT),
                             ])

    def test_only_italic_delimiter_split(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,)

    def test_only_code_delimiter_split(self):
        nodes_to_split = [
            TextNode("This is text with a `code block` word.", TextType.CODE),
            TextNode("Another line of text with some **Bold Words**",
                     TextType.BOLD),
            TextNode("*Italic* Example Block", TextType.ITALIC),
            TextNode("Checking for bold where there is none", TextType.BOLD),
            TextNode("Just some regular text", TextType.TEXT)
        ]

        code_splits = split_nodes_delimiter(nodes_to_split, "`", TextType.CODE)

        self.assertListEqual(code_splits,
                             [
                                 TextNode("This is text with a ",
                                          TextType.TEXT),
                                 TextNode("code block", TextType.CODE),
                                 TextNode(" word.", TextType.TEXT),
                                 TextNode(
                                     "Another line of text with some **Bold Words**", TextType.BOLD),
                                 TextNode("*Italic* Example Block",
                                          TextType.ITALIC),
                                 TextNode(
                                     "Checking for bold where there is none", TextType.BOLD),
                                 TextNode("Just some regular text",
                                          TextType.TEXT)
                             ])

    def test_multiple_splits(self):
        nodes_to_split = [
            TextNode("This is text with a `code block` word.", TextType.CODE),
            TextNode("Another line of text with some **Bold Words**",
                     TextType.BOLD),
            TextNode("*Italic* Example Block", TextType.ITALIC),
            TextNode("Checking for bold where there is none", TextType.BOLD),
            TextNode("Just some regular text", TextType.TEXT)
        ]

        code_splits = split_nodes_delimiter(nodes_to_split, "`", TextType.CODE)
        bold_splits = split_nodes_delimiter(code_splits, "**", TextType.BOLD)
        italic_splits = split_nodes_delimiter(
            bold_splits, "*", TextType.ITALIC)

        self.assertListEqual(italic_splits,
                             [
                                 TextNode("This is text with a ",
                                          TextType.TEXT),
                                 TextNode("code block", TextType.CODE),
                                 TextNode(" word.", TextType.TEXT),
                                 TextNode(
                                     "Another line of text with some ", TextType.TEXT),
                                 TextNode("Bold Words", TextType.BOLD),
                                 TextNode("Italic", TextType.ITALIC),
                                 TextNode(" Example Block", TextType.TEXT),
                                 TextNode(
                                     "Checking for bold where there is none", TextType.TEXT),
                                 TextNode("Just some regular text",
                                          TextType.TEXT)
                             ])

    def test_extract_images(self):
        images_text = "This is text with images of ![CN Tower](https://shorturl.at/gKQ3x) and ![Montreal Skyline](https://shorturl.at/d9Vxl)"
        self.assertListEqual(extract_markdown_images(images_text),
                             [
            ("CN Tower", "https://shorturl.at/gKQ3x"),
            ("Montreal Skyline", "https://shorturl.at/d9Vxl")
        ])

    def test_extract_links(self):
        links_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_markdown_links(links_text),
                             [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ])

    def test_extract_images_no_alt_or_link(self):
        images_text2 = "This is text with no discernable alt_text nor links"
        self.assertListEqual(extract_markdown_images(images_text2), [])


    def test_split_node_images(self):
        node_with_images = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node_with_images]),
                             [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

    def test_split_node_links(self):
        node_with_links = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and then some more text",
            TextType.TEXT,)
        self.assertListEqual(split_nodes_link([node_with_links]),
                             [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK,
                     "https://www.youtube.com/@bootdotdev"),
            TextNode(" and then some more text", TextType.TEXT),
        ]
        )

    def test_split_node_img_and_link(self):
        node_with_img_and_link = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and an image of ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) OBI WAN.",
            TextType.TEXT,)
        split_nodes_img = split_nodes_image([node_with_img_and_link])
        split_node_link = split_nodes_link(split_nodes_img)

        self.assertListEqual(split_node_link,
                             [
                                 TextNode("This is text with a link ",
                                          TextType.TEXT),
                                 TextNode("to boot dev", TextType.LINK,
                                          "https://www.boot.dev"),
                                 TextNode(" and an image of ", TextType.TEXT),
                                 TextNode("obi wan", TextType.IMAGE,
                                          "https://i.imgur.com/fJRm4Vk.jpeg"),
                                 TextNode(" OBI WAN.", TextType.TEXT),
                             ])

    def test_split_node_repli_images(self):
        node_with_images = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and again another ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node_with_images]),
                             [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and again another ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
        ])


    def test_text_to_text_nodes(self):
        test_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        to_text_nodes = convert_text_to_textnodes(test_text)
        self.assertListEqual(to_text_nodes,
                             [
                                 TextNode("This is ", TextType.TEXT),
                                 TextNode("text", TextType.BOLD),
                                 TextNode(" with an ", TextType.TEXT),
                                 TextNode("italic", TextType.ITALIC),
                                 TextNode(" word and a ", TextType.TEXT),
                                 TextNode("code block", TextType.CODE),
                                 TextNode(" and an ", TextType.TEXT),
                                 TextNode("obi wan image", TextType.IMAGE,
                                          "https://i.imgur.com/fJRm4Vk.jpeg"),
                                 TextNode(" and a ", TextType.TEXT),
                                 TextNode("link", TextType.LINK,
                                          "https://boot.dev"),
                             ])
        

    test_case = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""


if __name__ == "__main__":
    unittest.main()
