from Enums import TextType
from urllib.parse import urlparse

class TextNode:
    def __init__(self, text, text_type, url):

        if not isinstance(text_type, TextType):
            raise TypeError("Invalid Text Type")
        
        if url and not uri_validator(url):
            raise ValueError("URL is invalid!")

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


def main():
    textNodeExample = TextNode("Example TextNode",  TextType.ITALIC, "https://www.theweathernetwork.com")
    print(textNodeExample)

if __name__ == "__main__":
    main()