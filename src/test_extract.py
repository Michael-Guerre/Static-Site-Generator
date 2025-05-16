import unittest
from main import extract_markdown_links, extract_markdown_images,split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestExtractFunctions(unittest.TestCase):

    def test_extract_markdown_links(self):
        markdown_text = """
        [GitHub](https://github.com)
        [Python](https://www.python.org)
        ![image](https://example.com/image.png)
        """
        expected_links = [
            ("GitHub", "https://github.com"),
            ("Python", "https://www.python.org")
        ]
        self.assertEqual(extract_markdown_links(markdown_text), expected_links)

    def test_extract_markdown_images(self):
        markdown_text = """
        ![Alt text](https://example.com/image.jpg)
        ![Another image](https://example.com/another_image.png)
        [Python](https://www.python.org)
        """
        expected_images = [
            ("Alt text", "https://example.com/image.jpg"),
            ("Another image", "https://example.com/another_image.png")
        ]
        self.assertEqual(extract_markdown_images(markdown_text), expected_images)

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[3].text, "second image")

    def test_split_nodes_link(self):
        node = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[3].text, "second image")

    def test_split_nodes_link(self):
        node = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png) and more text",TextType.TEXT )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[3].text, "second image")
        self.assertEqual(new_nodes[4].text, " and more text")


    def test_split_nodes_link(self):
        node = TextNode("This is text without an image",TextType.TEXT )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text without an image")

    def test_split_nodes_link(self):
        node = TextNode("This is text with a wrong ![image",TextType.TEXT )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with a wrong ![image")


if __name__ == '__main__':
    unittest.main()