from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

# lookup table fort text types vs delimiters
text_type_delimiters = {
    text_type_bold: "**",
    text_type_italic: "*",
    text_type_code: "`",
    text_type_link: "[",
    text_type_image: "![",
}


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case text_type_text:
            return LeafNode(None, text_node.text)
        case text_type_bold:
            return LeafNode("b", text_node.text)
        case text_type_italic:
            return LeafNode("i", text_node.text)
        case  text_type_code:
            return LeafNode("code", text_node.text)
        case text_type_link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case text_type_image:
            return LeadNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid Text Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            # Split the text node based on the delimiter

        else:
            new_nodes.append(node)
    return new_nodes
