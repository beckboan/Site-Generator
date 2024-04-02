from textmanager import markdown_to_html_node, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode
import os

def generate_page(from_path, template_path, dest_path):
	
	with open(from_path, "r") as f:
		text = f.read()
	with open(template_path, "r") as f:
		template = f.read()

	page_node = markdown_to_html_node(text)
	print(page_node)
	contents = page_node.to_html()
	# print(contents)
	
	title = extract_title(text) 

	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", contents)

	with open(dest_path, "w") as f:
		f.write(template)
	
