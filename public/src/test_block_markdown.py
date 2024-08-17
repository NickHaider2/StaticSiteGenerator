import unittest
from block_markdown import markdown_to_blocks, block_to_block_type
from Enums import BlockType


class TestBlockMarkdown(unittest.TestCase):

    def test_single_markdown(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks = markdown_to_blocks(markdown)

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
        blocks = markdown_to_blocks(markdown)

        self.assertListEqual(blocks,
                             [
                                 "# This is a heading",
                                 "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                                 "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                             ])
        
    def test_block_to_blocktype(self):
        block = "### This is a heading."
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.HEADING)

        block = "```Some Code```"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.CODE)

        block = "> Some Quote\n> Another Quote\n> And Another Quote"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.QUOTE)

        block = "* First Item\n* Second Item\n* Third Item"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.UL_LIST)

        block = "- First Item\n- Second Item\n- Third Item"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.UL_LIST)

        block = "1. First Item\n2. Second Item\n3. Third Item"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.O_LIST)

        block = "1. First Item\n*. Second Item\n3. Third Item"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)
