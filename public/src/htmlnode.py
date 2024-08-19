class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        '''
        tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        children - A list of HTMLNode objects representing the children of this node
        props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        '''
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return "".join(f' {k}="{v}"' for k, v in self.props.items()) if self.props else ""
    
    def __repr__(self):
        return f"HTMLNode (tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value="", children=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Invalid HTML: LeafNode must have a value.")
        
        if not self.tag:
            return str(self.value)
        else:
            return f"<{str(self.tag)}{self.props_to_html()}>{str(self.value)}</{str(self.tag)}>"
        
    def __repr__(self):
        return f"LeafNode (tag: {self.tag}, value: {self.value}, props: {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):

        if not self.tag:
            raise ValueError("Invalid HTML: ParetNode must have a tag.")

        if not self.children:
             raise ValueError("Invalid HTML: ParentNode must have a list of children.")
        
        return f"<{str(self.tag)}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{str(self.tag)}>"


    def __repr__(self):
        return f"ParentNode (tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
            

def main():
    HTML_node = HTMLNode("div", "This is the middle div", [], {"text-align": "center"})
    print(HTML_node)   

    leaf_node = LeafNode("p", "This is a paragraph", [], {"class": "exciting-paragraph"})
    print(leaf_node.to_html())

    children1 = [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    ]

    parent_node = ParentNode(
                            "p",
                            children1,
                        )
    print(parent_node.to_html())

    parent_node2 = ParentNode("h1", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    ParentNode("h2", [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text")]),
                    ])
    print(parent_node2.to_html())
    

if __name__ == "__main__":
    main()

