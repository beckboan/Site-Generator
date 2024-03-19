
import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Hello",
            None,
            {"class": "nice", "href": "https://website.com"},
        )

        self.assertEqual(node.props_to_html(),
                         ' class="nice" href="https://website.com"')


if __name__ == "__main__":
    unittest.main()
