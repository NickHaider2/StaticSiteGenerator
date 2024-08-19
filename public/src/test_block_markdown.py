import unittest
from block_markdown import convert_markdown_to_blocks, determine_block_type, convert_markdown_to_html_node
from Enums import BlockType


class TestBlockMarkdown(unittest.TestCase):

    def test_single_markdown(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks = convert_markdown_to_blocks(markdown)

        self.assertListEqual(blocks,
                             [
                                 "# This is a heading",
                                 "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                                 "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                             ])

    def test_markdown_with_multiple_newlines(self):
        markdown = """# This is a heading

    



This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = convert_markdown_to_blocks(markdown)

        self.assertListEqual(blocks,
                             [
                                 "# This is a heading",
                                 "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                                 "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                             ])
        
    def test_determine_block_type(self):
        test_cases = [
            ("### This is a heading.", BlockType.HEADING), 
            ("```Some Code```", BlockType.CODE),
            ("> Some Quote\n> Another Quote\n> And Another Quote", BlockType.QUOTE),
            ("* First Item\n* Second Item\n* Third Item", BlockType.U_LIST),
            ("- First Item\n- Second Item\n- Third Item", BlockType.U_LIST),
            ("1. First Item\n2. Second Item\n3. Third Item", BlockType.O_LIST),
            ("1. First Item\n*. Second Item\n3. Third Item", BlockType.PARAGRAPH),
            ("This is a paragraph with\nsome text", BlockType.PARAGRAPH)
        ]
        for test_case, expected_block_type in test_cases:
            self.assertEqual(determine_block_type(test_case), expected_block_type)


class TestBlockToHTML(unittest.TestCase):
    def test_markdown_to_html_node(self):
        test_cases = [
            ("### This is a heading.", "h3"),
            ("```python\nprint('Hello World!')\n```", "pre"),
            ("> Some Quote\n> Another Quote\n> And Another Quote", "blockquote"),
            ("This is a paragraph\nof text.\nIt has some **bold** and *italic* words inside of it.", "p"),
            ("* First Item\n* Second Item\n* Third Item", "ul"),
            ("- First Item\n- Second Item\n- Third Item", "ul"),
            ("1. First Item\n2. Second Item\n3. Third Item", "ol"),
        ]
        for test_block, expected_tag in test_cases:
            markdown_html_node = convert_markdown_to_html_node(test_block)
            # print(markdown_html_node)
            self.assertEqual(markdown_html_node.children[0].tag, expected_tag)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = convert_markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = convert_markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = convert_markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = convert_markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = convert_markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )