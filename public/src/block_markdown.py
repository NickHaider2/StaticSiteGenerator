import re
from Enums import BlockType
from functools import reduce


def markdown_to_blocks(markdown):

    markdown_blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in markdown_blocks if block and not block.isspace()]
    blocks = list(map(lambda block: re.sub(r'\n\s+', '\n', block.strip()), blocks))

    # print(f"Blocks:\n{blocks}")

    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    
    if re.match(r"^`{3}[\s\S]+`{3}$", block):       # and re.match(r"`{3}$", block):
        return BlockType.CODE
    
    lines = block.splitlines()
    if all(re.match(r"^>", line) for line in lines):
        return BlockType.QUOTE
    
    if all(re.match(r"^\*\s", line) for line in lines):
        return BlockType.UL_LIST
    
    if all(re.match(r"^-\s", line) for line in lines):
        return BlockType.UL_LIST
    
    if all(re.match(rf"^{i}. ", line) for i, line in enumerate(lines, start=1)):
        return BlockType.O_LIST

    return BlockType.PARAGRAPH
    
def main():
    pass

if __name__ == "__main__":
    main()


