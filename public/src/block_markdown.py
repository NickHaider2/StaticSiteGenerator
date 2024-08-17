import re


def markdown_to_blocks(markdown):

    markdown_blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in markdown_blocks if block and not block.isspace()]
    blocks = list(map(lambda block: re.sub(r'\n\s+', '\n', block.strip()), blocks))

    # print(f"Blocks:\n{blocks}")

    return blocks

def main():
    pass

if __name__ == "__main__":
    main()


