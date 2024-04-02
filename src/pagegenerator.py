from textmanager import markdown_to_html_node, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode
import os

def generate_page(from_path, template_path, dest_path):
	
	with open(from_path, "r") as f:
		text = f.read()
	with open(template_path, "r") as f:
		template = f.read()

	page_node = markdown_to_html_node(text)
	contents = page_node.to_html()
	# print(contents)
	
	title = extract_title(text) 

	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", contents)

	with open(dest_path, "w") as f:
		f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	for item in os.listdir(dir_path_content):
		s = os.path.join(dir_path_content, item)
		d = os.path.join(dest_dir_path, item)
		if os.path.isdir(s):
			os.mkdir(d)
			generate_pages_recursive(s, template_path, d)
		else:
			if item.endswith(".md"):
				new_item = item.replace(".md", ".html")
				new_dest = os.path.join(dest_dir_path, new_item)
				generate_page(s, template_path, new_dest)
	
