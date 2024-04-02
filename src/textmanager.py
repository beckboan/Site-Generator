from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

import re


class TextTypes:
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"


def text_node_to_html_node(text_node):
    if text_node.text is None:
        raise ValueError("Text Node has no text")
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
            return LeafNode("img", text_node.text, {"src": text_node.url,
                                          "alt": text_node.text})
        case _:
            raise ValueError("Invalid Text Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.text:
            text = node.text
            parts = text.split(delimiter)
            #See how many parts we have
            #Len of parts must be odd to have a delimiter pair
            if len(parts) % 2 == 0:
                raise ValueError("Delimiter without pair")
            else:
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        if part != "":
                            new_nodes.append(TextNode(part, TextTypes.text))
                    else:
                        new_nodes.append(TextNode(part, text_type))


        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    # ![text](url)
    match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    results = []

    if match is None:
        return []

    for m in match:
        results.append(tuple([m[0], m[1]]))
    
    return results


def extract_markdown_links(text):
    # [text](url)
    match = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    if match is None:
        return []
    results = []

    for m in match:
        results.append(tuple([m[0], m[1]]))
    
    return results


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.text:
            text = node.text
            images = extract_markdown_images(text)
            if images == []:
                new_nodes.append(node)
            else:
                end_text = text
                for image in images:
                    textsplit = end_text.split(f"![{image[0]}]({image[1]})", 1)
                    end_text = textsplit[-1]
                    if (textsplit[0] != ""):
                        new_nodes.append(TextNode(textsplit[0], TextTypes.text))
                    new_nodes.append(TextNode(image[0], TextTypes.image, image[1]))
                if (end_text != ""):
                    new_nodes.append(TextNode(end_text, TextTypes.text))
        else:
            if (node.text != ""):
                new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.text:
            text = node.text
            links = extract_markdown_links(text)
            if links == []:
                new_nodes.append(node)
            else:
                end_text = text
                for link in links:
                    textsplit = end_text.split(f"[{link[0]}]({link[1]})", 1)
                    end_text = textsplit[-1]
                    if (textsplit[0] != ""):
                        new_nodes.append(TextNode(textsplit[0], TextTypes.text))
                    new_nodes.append(TextNode(link[0], TextTypes.link, link[1]))
                if (end_text != ""):
                    new_nodes.append(TextNode(end_text, TextTypes.text))
        else:
            if (node.text != ""):
                new_nodes.append(node)
        
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextTypes.text)]
    try:
        text_nodes = split_nodes_delimiter(text_nodes, "**", TextTypes.bold)
        text_nodes = split_nodes_delimiter(text_nodes, "*", TextTypes.italic)
        text_nodes = split_nodes_delimiter(text_nodes, "`", TextTypes.code)
        text_nodes = split_nodes_image(text_nodes)
        text_nodes = split_nodes_link(text_nodes)
    except ValueError as e:
        print("Error: ", e)
        pass

    return text_nodes

def markdown_to_blocks(markdown):
    blocks= []
    split = markdown.split("\n\n")
    for line in split:
        #Remove \n at beginning and end of line
        line = line.strip().strip("\n").strip()
        if line != "":
            blocks.append(line)

    return blocks

class BlockTypes:
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(block):
    if block.startswith("#"):
        for i in range(1, 7):
            if block.startswith("#" * i + " "):
                return BlockTypes.heading

    if block.startswith("```") and block.endswith("```"):
        return BlockTypes.code

    block_lines = block.split("\n")
    block_lines = [line.strip() for line in block_lines]

    line_count = len(block_lines)
    for line in block_lines:
        if line.startswith(">"):
            line_count -= 1
    if line_count == 0:
        return BlockTypes.quote

    line_count = len(block_lines)
    for line in block_lines:
        if line.startswith("*") or line.startswith("-"):
            line_count -= 1
    if line_count == 0:
        return BlockTypes.unordered_list
    
    line_count = len(block_lines)
    for index, line in enumerate(block_lines):
        if line.startswith(f"{index + 1}."):
            line_count -= 1
    if line_count == 0:
        return BlockTypes.ordered_list

    return BlockTypes.paragraph

def paragraph_block_to_html(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode("p", html_nodes)

def heading_block_to_html(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    heading_count = len(block) - len(block.lstrip("#"))
    return ParentNode(f"h{heading_count}", html_nodes)

def code_block_to_html(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode("code", ParentNode("pre", html_nodes))

def quote_block_to_html(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode("blockquote", html_nodes)

def ul_block_to_html(block):
    items = block.split("\n")
    items = [item.strip().strip("*").strip("-") for item in items]
    text_nodes = [text_to_textnodes(item) for item in items]
    html_nodes = []
    for nodes in text_nodes:
        html_nodes.append(LeafNode("li", [text_node_to_html_node(node) for node in nodes]))
    return ParentNode("ul", html_nodes)



def ol_block_to_html(block):
    items = block.split("\n")
    for i, item in enumerate(items):
        items[i] = item.strip().strip(f"{i + 1}.").strip()
    text_nodes = [text_to_textnodes(item) for item in items]
    html_nodes = []
    for nodes in text_nodes:
        html_nodes.append(LeafNode("li", [text_node_to_html_node(node) for node in nodes]))
    return ParentNode("ol", html_nodes)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockTypes.paragraph:
            html_nodes.append(paragraph_block_to_html(block))
        elif block_type == BlockTypes.heading:
            html_nodes.append(heading_block_to_html(block))
        elif block_type == BlockTypes.code:
            html_nodes.append(code_block_to_html(block))
        elif block_type == BlockTypes.quote:
            html_nodes.append(quote_block_to_html(block))
        elif block_type == BlockTypes.unordered_list:
            html_nodes.append(ul_block_to_html(block))
        elif block_type == BlockTypes.ordered_list:
            html_nodes.append(ol_block_to_html(block))

    return ParentNode("div", html_nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if len(blocks) == 0:
        raise ValueError("No header found")
    count = 0
    title = ""
    for block in blocks:
        if block.startswith("# "):
            count += 1
            title = block.strip("# ").strip()
    if count == 0:
        raise ValueError("No header found")
    if count > 1:
        raise ValueError("Multiple headers found")
    return title


