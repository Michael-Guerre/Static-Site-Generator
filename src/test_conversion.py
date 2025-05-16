import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from main import markdown_to_html_node, text_node_to_html_node,text_to_textnodes,markdown_to_block
from textnode import TextNode, TextType

class TestConverion(unittest.TestCase):

    def test_bold_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.BOLD)
        node = LeafNode("b", "This is a text node")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), node.to_html())
    
    
    def test_link_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.LINKS,"google.com")
        node = LeafNode("a", "This is a text node", {"href": "google.com"})
        self.assertEqual(text_node_to_html_node(text_node).to_html(), node.to_html())
    
    
    def test_normal_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        node = LeafNode(None, "This is a text node")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), node.to_html())

    def test_italic_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.ITALIC)
        node = LeafNode("i", "This is a text node")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), node.to_html())
    
    def test_code_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.CODE)
        node = LeafNode("code", "This is a text node")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), node.to_html())
    
    def test_image_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.IMAGE,"image.jpg")
        node = LeafNode("img", "This is a text node", {"src": "image.jpg"})
        self.assertEqual(text_node_to_html_node(text_node).to_html(), node.to_html())

    def test_split_nodes_delimiter(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",TextType.TEXT )
        new_nodes = text_to_textnodes([node])
        correct_nodes = [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINKS, "https://boot.dev"),
                        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_markdown_to_block(self):
        markdown_text = """
        # Heading 1

        This is a paragraph with **bold text**, _italic text_, and a [link](https://example.com).

        ## Heading 2

        - Item 1
        - Item 2
        - Item 3

        ![Image description](https://example.com/image.jpg)
        """
        blocks = markdown_to_block(markdown_text)
        expected_blocks = [
            "# Heading 1",
            "This is a paragraph with **bold text**, _italic text_, and a [link](https://example.com).",
            "## Heading 2",
            """- Item 1
- Item 2
- Item 3""",
            "![Image description](https://example.com/image.jpg)",
        ]
        self.assertEqual(blocks, expected_blocks)

        def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_codeblock(self):
            md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

    def test_unordered_list(self):
        md = """
## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Reasons I like Tolkien</h2><ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <i>didn't ruin it</i> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul></div>",
        )