import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("Node", "bold")
        node2 = TextNode("Node", "bold")
        self.assertEqual(node, node2)

    def test_empty_url(self):
        node = TextNode("Node", "bold", "http://website.com")
        self.assertIsNotNone(node.url)
        node2 = TextNode("Node", "bold")
        self.assertIsNone(node2.url)

    def test_diff_txt(self):
        node = TextNode("Node", "italics")
        node2 = TextNode("Node", "bold")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Node", "bold", "https://website.com")
        self.assertEqual(
            "TextNode(Node, bold, https://website.com)", repr(node))


if __name__ == "__main__":
    unittest.main()
