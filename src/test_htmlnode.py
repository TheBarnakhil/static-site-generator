import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_node(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node1 = HTMLNode("h1", props=props)

        self.assertEqual(node1.tag , "h1")
        self.assertIsNone(node1.children)
        self.assertIsNone(node1.value)
        self.assertDictEqual(props , node1.props)
    
    def test_node_all(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        nodeChild = HTMLNode("h1", "This is raw text" , props=props)
        nodeParent = HTMLNode("h1", children=[nodeChild] , props=props)

        self.assertEqual(nodeChild.tag , "h1")
        self.assertEqual(nodeParent.tag , "h1")
        self.assertIsNone(nodeChild.children)
        self.assertIsNone(nodeParent.value)
        self.assertDictEqual(props , nodeChild.props)
        self.assertDictEqual(props , nodeParent.props)
        self.assertIn(nodeChild, nodeParent.children)
    
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode(props=props)

        value = node.props_to_html()
        self.assertIn(" href", value)
        self.assertIn("https://www.google.com", value)
        self.assertIn(" target", value)
        self.assertIn("_blank", value)
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )
    

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a_attr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode(tag="a", value="Hello, world!", props=props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Hello, world!</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()