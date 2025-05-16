import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode('div')
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_init_with_values(self):
        node = HTMLNode('p', 'Hello', [HTMLNode('span')], {'class': 'text'})
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Hello')
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, 'span')
        self.assertEqual(node.props, {'class': 'text'})

    def test_props_to_html(self):
        node = HTMLNode('a', props={'href': 'https://example.com', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), ' href= "https://example.com"  target= "_blank" ')

    def test_repr(self):
        node = HTMLNode('div', props={'id': 'main'})
        self.assertEqual(repr(node), "div {'id': 'main'} [] {'id': 'main'}")


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode('h1', 'Hello', {'class': 'heading'})
        self.assertEqual(node.tag, 'h1')
        self.assertEqual(node.value, 'Hello')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'class': 'heading'})

    def test_ValueError(self):
        with self.assertRaises(ValueError):
            LeafNode('img',None).to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, 'Hello')
        self.assertEqual(node.to_html(), 'Hello')

    def test_to_html(self):
        node = LeafNode('h1', 'Hello', props={'class': 'heading'})
        self.assertEqual(node.to_html(), '<h1 class= "heading" >Hello</h1>')

    def test_to_html_no_value(self):
        node = LeafNode('img',None, props={'src': 'image.jpg'})
        with self.assertRaises(ValueError):
            node.to_html()
    

class TestParentNode(unittest.TestCase):
    def test_init(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_ValueError_No_Tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None,[LeafNode("b", "Bold text")]).to_html()

    def test_ValueError_No_Children(self):
        with self.assertRaises(ValueError):
            ParentNode("p",None).to_html()

    def test_parent_in_parent(self):
        node = ParentNode(
            "p",
            [
                ParentNode("div",[
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ])
            ],
        )
        self.assertEqual(node.to_html(),"<p><div><b>Bold text</b>Normal text<i>italic text</i>Normal text</div></p>")

        

if __name__ == "__main__":
    unittest.main()