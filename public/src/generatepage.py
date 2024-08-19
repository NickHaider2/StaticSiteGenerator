from block_markdown import convert_markdown_to_blocks, determine_block_type, convert_markdown_to_html_node
from Enums import BlockType
import os

def extract_title(markdown):
    blocks = convert_markdown_to_blocks(markdown)

    for block in blocks:
        if determine_block_type(block) == BlockType.HEADING:
            if block.startswith("# "):
                return block[2:]
            
    raise ValueError("No Title found in markdown.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page using template: {template_path}, from {from_path} to {dest_path}.")

    with open(from_path, 'r') as file:
        markdown = file.read()
        file.close()

    with open(template_path, 'r') as file:
        template = file.read()
        file.close()

    html = convert_markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page_contents = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    html_page = open(dest_path, "w")
    html_page.write(page_contents)
    html_page.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        print(f"Path created: {dest_dir_path}")

    for content in os.listdir(dir_path_content):
        content_src_path = os.path.join(dir_path_content, content)
        new_dir_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(content_src_path):
            new_dir_path = new_dir_path.rstrip(".md") + ".html"
            print(f"Content: {content_src_path} copied to Destination: {new_dir_path}")
            generate_page(content_src_path, template_path, new_dir_path)
        else:
            generate_pages_recursive(content_src_path, template_path, new_dir_path)
