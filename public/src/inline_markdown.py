from Enums import TextType
from textnode import TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:

        if delimiter not in node.text:
            if node.text_type == text_type:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            # print(parts)
            if len(parts) % 2 == 0:
                raise SyntaxError(
                    "Invalid Markdown Syntax: non-matching closing delimiter")

            for i, part in enumerate(parts):
                if part == "":
                    continue
                elif i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        matches = extract_markdown_links(old_node.text)

        if not matches:
            new_nodes.append(old_node)
            continue

        temp_nodes = [old_node]
        candidate_nodes = temp_nodes

        for match in matches:
            link_text, link_url = match
            temp_nodes = []
            found = True

            while found:
                for node in candidate_nodes:
                    found = False

                    if node.text_type == TextType.LINK or f"[{link_text}]({link_url})" not in node.text:
                        temp_nodes.append(node)
                        continue

                    found = True
                    node_split = node.text.split(
                        f"[{link_text}]({link_url})", 1)

                    if node_split[0] != "":
                        temp_nodes.append(
                            TextNode(node_split[0], TextType.TEXT))

                    temp_nodes.append(
                        TextNode(f"{link_text}", TextType.LINK, f"{link_url}"))

                    if node_split[1] != "":
                        temp_nodes.append(
                            TextNode(node_split[1], TextType.TEXT))

                candidate_nodes = temp_nodes
                temp_nodes = []

        new_nodes.extend(candidate_nodes)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        matches = extract_markdown_images(old_node.text)

        if not matches:
            new_nodes.append(old_node)
            continue

        temp_nodes = [old_node]
        candidate_nodes = temp_nodes

        for match in matches:
            link_text, link_url = match
            temp_nodes = []
            found = True

            while found:
                for node in candidate_nodes:
                    found = False

                    if node.text_type == TextType.IMAGE or f"![{link_text}]({link_url})" not in node.text:
                        temp_nodes.append(node)
                        continue

                    found = True
                    node_split = node.text.split(
                        f"![{link_text}]({link_url})", 1)

                    if node_split[0] != "":
                        temp_nodes.append(
                            TextNode(node_split[0], TextType.TEXT))

                    temp_nodes.append(
                        TextNode(f"{link_text}", TextType.IMAGE, f"{link_url}"))

                    if node_split[1] != "":
                        temp_nodes.append(
                            TextNode(node_split[1], TextType.TEXT))

                candidate_nodes = temp_nodes
                temp_nodes = []

        new_nodes.extend(candidate_nodes)

    return new_nodes


def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    bold_processed_text = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    italic_processed_text = split_nodes_delimiter(bold_processed_text, "*", TextType.ITALIC)
    code_processed_text = split_nodes_delimiter(italic_processed_text, "`", TextType.CODE)
    image_split_text = split_nodes_image(code_processed_text)
    link_split_text = split_nodes_link(image_split_text)
    return link_split_text

def main():

    nodes_to_split = [
        TextNode("This is text with a `code block` word.", TextType.CODE),
        TextNode("Another line of text with some **Bold Words**", TextType.BOLD),
        TextNode("*Italic* Example Block", TextType.ITALIC),
        TextNode("Checking for bold where there is none", TextType.BOLD),
        TextNode("Just some regular text", TextType.TEXT)
    ]

    code_splits = split_nodes_delimiter(nodes_to_split, "`", TextType.CODE)
    bold_splits = split_nodes_delimiter(code_splits, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_splits, "*", TextType.ITALIC)
    print("\n".join(repr(split) for split in italic_split))

    image_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(image_text))

    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(link_text))

    node_with_links = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and then some more text",
        TextType.TEXT,)
    print(split_nodes_link([node_with_links]))

    node_with_images = TextNode(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
    print(split_nodes_image([node_with_images]))

    test_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(test_text))


if __name__ == "__main__":
    main()
