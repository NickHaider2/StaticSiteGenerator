import re
from Enums import BlockType
from htmlnode import ParentNode
from inline_markdown import convert_text_to_textnodes
from textnode import convert_text_node_to_html_node


def convert_markdown_to_blocks(markdown):

    markdown_blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in markdown_blocks if block and not block.isspace()]
    blocks = list(map(lambda block: re.sub(r'\n\s+', '\n', block.strip()), blocks))

    # print(f"Blocks:\n{blocks}")

    return blocks

def determine_block_type(block):
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    
    if re.match(r"^`{3}[\s\S]+`{3}$", block):
        return BlockType.CODE
    
    lines = block.splitlines()
    if all(re.match(r"^>", line) for line in lines):
        return BlockType.QUOTE
    
    if all(re.match(r"^\*\s", line) for line in lines):
        return BlockType.U_LIST
    
    if all(re.match(r"^-\s", line) for line in lines):
        return BlockType.U_LIST
    
    if all(re.match(rf"^{i}. ", line) for i, line in enumerate(lines, start=1)):
        return BlockType.O_LIST

    return BlockType.PARAGRAPH
    
def convert_markdown_to_html_node(markdown):
    html_node = ParentNode("div", children = [])
    blocks = convert_markdown_to_blocks(markdown)
    converters = {
        BlockType.HEADING: convert_heading_to_html_node,
        BlockType.PARAGRAPH: convert_paragraph_to_html_node,
        BlockType.QUOTE: convert_quote_to_html_node,
        BlockType.CODE: convert_code_to_html_node,
        BlockType.U_LIST: convert_unordered_list_to_html_node,
        BlockType.O_LIST: convert_ordered_list_to_html_node,
    }

    for block in blocks:
        block_type = determine_block_type(block)

        if block_type not in converters:
            raise ValueError("Invalid Block Type.")
    
        else:
            html_node.children.append(converters[block_type](block))
        
    return html_node

def convert_paragraph_to_html_node(block):
    block = block.replace("\n", " ")
    return ParentNode("p", children = convert_text_to_children(block))

def convert_heading_to_html_node(block):
    hash_counter = 0
    for i, char in enumerate(block):
        if char == "#":
            hash_counter += 1
        else:
            break
    
    heading_text = block[hash_counter+1:]
    return ParentNode(f"h{hash_counter}", children = convert_text_to_children(heading_text))

def convert_quote_to_html_node(block):
    processed_block = block.replace("> ", "").replace(">", "").replace("\n", " ")
    block_nodes = convert_text_to_children(processed_block)
    return ParentNode("blockquote", children = block_nodes)

def convert_code_to_html_node(block):
    code_text = block[3:-3]
    code_html_node = ParentNode("code", children = convert_text_to_children(code_text))
    return ParentNode("pre", children = [code_html_node])

def convert_unordered_list_to_html_node(block):
    list_text_nodes = block.splitlines()
    for i, line in enumerate(list_text_nodes):
        list_text_nodes[i] = ParentNode("li", children = convert_text_to_children(line.lstrip("* ").lstrip("- ")))

    return ParentNode("ul", children = list_text_nodes)

def convert_ordered_list_to_html_node(block):
    list_text_nodes = block.splitlines()
    for i, line in enumerate(list_text_nodes, start=1):
        list_text_nodes[i-1] = ParentNode("li",  children = convert_text_to_children(line.lstrip(f"{i}. ")))

    return ParentNode("ol", children = list_text_nodes)

def convert_text_to_children(text):
    '''Convert text to a list of HTML LeafNodes'''
    text_nodes = convert_text_to_textnodes(text)
    html_nodes = [convert_text_node_to_html_node(text_node) for text_node in text_nodes]
    return html_nodes

def main():
    pass

if __name__ == "__main__":
    main()


