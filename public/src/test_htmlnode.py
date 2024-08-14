import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode

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

    
    
if __name__ == "__main__":
    unittest.main()
