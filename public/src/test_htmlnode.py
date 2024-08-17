import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("h1", "heading1", [], {})
        node2 = HTMLNode("h1", "heading1", [], {})

        self.assertEqual(node1.tag, node2.tag)
        self.assertEqual(node1.value, node2.value)
        self.assertEqual(node1.children, node2.children)
        self.assertEqual(node1.props, node2.props)

    def test_repr(self):
        # node2 = HTMLNode("h1", "heading1", [], {})
        node1 = HTMLNode("h3", "Some Random Text", [], {"text-align": "left"} )

        self.assertEqual(repr(node1), 
                         "HTMLNode (tag: h3, value: Some Random Text, children: [], props: {'text-align': 'left'})"
                         )

    def test_props_to_html(self):
        node1 = HTMLNode("h3", "Some Random Text", [], {"text-align": "left", "a": "https://www.weathernetwork.com"} )
        props_to_html_string = node1.props_to_html()

        self.assertEqual(props_to_html_string, 
                          ' text-align="left" a="https://www.weathernetwork.com"'
                          )
        
    def assert_leaf_has_value(self):
        leaf_node = LeafNode("p", "", [], {"text-align": "left"})
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_no_tag(self):
        leaf_node = LeafNode("", "Random Value", [], {"text-align": "left"})
        self.assertEqual(leaf_node.to_html(), "Random Value")
    
    def test_to_html(self):
        leaf_node = LeafNode("a", "Click Me!", [], {"href": "https://www.weathernetwork.com"})
        self.assertEqual(leaf_node.to_html(), '<a href="https://www.weathernetwork.com">Click Me!</a>' )

    
    def test_parent_no_children(self):
        parent_node = ParentNode("p", None, {"text-align": "left"})
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_multiple_children(self):
        parent_node = ParentNode("p", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    ], {"text-align": "left"})
        self.assertEqual(parent_node.to_html(),
                         '<p text-align="left"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
    
    def test_parent_with_grandchildren(self):
        parent_node = ParentNode("h1", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    ParentNode("h2", [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text")]),
                    ])
        self.assertEqual(parent_node.to_html(), "<h1><b>Bold text</b>Normal text<i>italic text</i><h2><b>Bold text</b>Normal text</h2></h1>")
        
    
if __name__ == "__main__":
    unittest.main()
