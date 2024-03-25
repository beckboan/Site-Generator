import unittest

from textmanager import split_nodes_delimiter, TextTypes
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


if __name__ == "__main__":
    unittest.main()
