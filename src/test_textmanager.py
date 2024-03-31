import unittest

from textmanager import split_nodes_delimiter, TextTypes, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from htmlnode import HTMLNode
from textnode import TextNode


class TestTextManager(unittest.TestCase):
    def test_eq(self):
        node = TextNode(
            "This is text with a `code block` word", TextTypes.text)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextTypes.text),
                TextNode("code block", TextTypes.code),
                TextNode(" word", TextTypes.text),
            ],
        )

    def test_eq2(self):
        node = TextNode(
            "`This` is text with a code block word", TextTypes.text)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextTypes.code),
                TextNode(" is text with a code block word", TextTypes.text),
            ],
        )
    def test_double(self):
        node = TextNode(
            "`This` is text with a `code` block word", TextTypes.text)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextTypes.code),
                TextNode(" is text with a ", TextTypes.text),
                TextNode("code", TextTypes.code),
                TextNode(" block word", TextTypes.text),
            ],
        )
    def test_bold(self):
        node = TextNode(
		    "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)", TextTypes.text)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextTypes.text),
                TextNode("text", TextTypes.bold),
                TextNode(" with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)", TextTypes.text),
            ],
        )

    def test_no_pair(self):
        node = TextNode("This is text with a `code block word", TextTypes.text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextTypes.code)

    def test_no_nodes(self):
        new_nodes = split_nodes_delimiter([], "`", TextTypes.code)
        self.assertEqual(new_nodes, [])

    def test_HTMLNode(self):
        node = HTMLNode("div", "Hello")
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.code)
        self.assertEqual(new_nodes, [node])

    def test_extract_images(self):
        text = "![text](url)"
        self.assertEqual(extract_markdown_images(text), [("text", "url")])

    def test_extract_links(self):
        text = "[text](url)"
        self.assertEqual(extract_markdown_links(text), [("text", "url")])

    def test_split_image(self):
        node = TextNode("this is ![text](url) it", TextTypes.text)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("this is ", TextTypes.text),
                TextNode("text", TextTypes.image, url="url"),
                TextNode(" it", TextTypes.text),
            ],
        )

    def test_split_image2(self):
        node = TextNode("this is ![text](url) it ![text2](url2)", TextTypes.text)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("this is ", TextTypes.text),
                TextNode("text", TextTypes.image, url="url"),
                TextNode(" it ", TextTypes.text),
                TextNode("text2", TextTypes.image, url="url2"),
            ],
        )

    def test_split_link(self):
        node = TextNode("this is [text](url) it", TextTypes.text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("this is ", TextTypes.text),
                TextNode("text", TextTypes.link, url="url"),
                TextNode(" it", TextTypes.text),
            ],
        )

    def test_split_link2(self):
        node = TextNode("this is [text](url) it [text2](url2)", TextTypes.text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("this is ", TextTypes.text),
                TextNode("text", TextTypes.link, url="url"),
                TextNode(" it ", TextTypes.text),
                TextNode("text2", TextTypes.link, url="url2"),
            ],
        )

    def test_text_to_textnodes(self):
        self.maxDiff = None
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextTypes.text),
                TextNode("text", TextTypes.bold),
                TextNode(" with an ", TextTypes.text),
                TextNode("italic", TextTypes.italic),
                TextNode(" word and a ", TextTypes.text),
                TextNode("code block", TextTypes.code),
                TextNode(" and an ", TextTypes.text),
                TextNode("image", TextTypes.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextTypes.text),
                TextNode("link", TextTypes.link, "https://boot.dev"),
            ]
        )

    def test_markdown_to_blocks(self):
        markdown = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ]
        )


if __name__ == "__main__":
    unittest.main()
