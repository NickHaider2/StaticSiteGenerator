from urllib.parse import urlparse
from Enums import TextType
from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):

        if not isinstance(text_type, TextType):
            raise TypeError("Invalid Text Type")
        
        # if url and not uri_validator(url):
        #     raise ValueError("URL is invalid!")

        self.text = text
        self.text_type = text_type
        self.url = url
        

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def uri_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
    
def convert_text_node_to_html_node(text_node):

    if not isinstance(text_node.text_type, TextType):
            raise TypeError("Invalid Text Type")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, None, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, None, props={"src": text_node.url, "alt": text_node.text})
        

def main():
    textNodeExample = TextNode("Example TextNode",  TextType.ITALIC, "https://www.theweathernetwork.com")
    print(textNodeExample)

    print(convert_text_node_to_html_node(textNodeExample))

if __name__ == "__main__":
    main()