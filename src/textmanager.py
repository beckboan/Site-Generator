from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode


class TextTypes:
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextTypes.text:
            return LeafNode(None, text_node.text)
        case TextTypes.bold:
            return LeafNode("b", text_node.text)
        case TextTypes.italic:
            return LeafNode("i", text_node.text)
        case TextTypes.code:
            return LeafNode("code", text_node.text)
        case TextTypes.link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextTypes.image:
            return LeafNode("img", None, {"src": text_node.url,
                                          "alt": text_node.text})
        case _:
            raise ValueError("Invalid Text Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            text = node.text
            parts = text.split(delimiter)
            if len(parts) < 3:
                raise ValueError("Delimiter without pair")
            else:
                new_nodes.append(TextNode(parts[0], TextTypes.text))
                new_nodes.append(
                    TextNode(parts[1], text_type))
                new_nodes.append(TextNode(parts[2], TextTypes.text))

        else:
            new_nodes.append(node)
    return new_nodes
