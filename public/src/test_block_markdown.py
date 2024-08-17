import unittest
from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):

#     def test_single_markdown(self):
#         markdown = """# This is a heading

# This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# * This is the first list item in a list block
# * This is a list item
# * This is another list item"""

#         blocks = markdown_to_blocks(markdown)

#         self.assertListEqual(blocks,
#                              [
#                                  "# This is a heading",
#                                  "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
#                                  "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
#                              ])

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
