from htmlnode import LeafNode, ParentNode
from textnode import BlockType, TextNode,TextType
import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(None,text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", text_node.text, {"src": text_node.url})
    else:
        raise Exception("Unknown TextType")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter in node.text:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, node.text_type))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if "![" in node.text:
            list = extract_markdown_images(node.text)
            if not list:
                new_nodes.append(node)
                continue
            remaining_text = node.text
            for text,url in list:
                parts = remaining_text.split(f"![{text}]({url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.IMAGE,url))
                if len(parts) >1 :
                    remaining_text = parts[1]
                else:
                    remaining_text = ""
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if "[" in node.text:
            if "![" in node.text and extract_markdown_images(node.text):
                new_nodes.append(node)
                return new_nodes
            list = extract_markdown_links(node.text)
            if not list:
                new_nodes.append(node)
                continue
            remaining_text = node.text
            for text,url in list:
                parts = remaining_text.split(f"[{text}]({url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINKS,url))
                if len(parts) >1 :
                    remaining_text = parts[1]
                else:
                    remaining_text = ""
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes
    
def text_to_textnodes(text):
    text = text[0].text
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_block(markdown):
    text = markdown.split("\n\n")
    text = [text.strip() for text in text]
    cleaned_text = []
    for par in text:
        lines = par.split("\n")
        lines = [line.strip() for line in lines]
        par = "\n".join(lines)
        cleaned_text.append(par)
    cleaned_text = [t for t in cleaned_text if t]
    return cleaned_text

def block_to_block_type(block):
    if block.startswith("# "):
        return BlockType.HEADINGS
    elif block.startswith("## "):
        return BlockType.HEADINGS
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED
    elif block[0].isdigit() and block[1] == ".":
        return BlockType.ORDERED
    else:
        return BlockType.NORMAL

def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADINGS:
            if block.startswith("# "):
                node = LeafNode("h1", block[2:])
            elif block.startswith("## "):
                node = LeafNode("h2", block[3:])
            elif block.startswith("### "):
                node = LeafNode("h3", block[4:])
            elif block.startswith("#### "):
                node = LeafNode("h4", block[5:])
            elif block.startswith("##### "):
                node = LeafNode("h5", block[6:])
            elif block.startswith("###### "):
                node = LeafNode("h6", block[7:])
        elif block_type == BlockType.QUOTE:
            node = LeafNode("blockquote", block[2:])
        elif block_type == BlockType.UNORDERED:
            items = block.split("\n")
            children = []
            for item in items:
                if item.startswith("- "):
                    node_child = ParentNode("li",[])
                    test = text_to_textnodes([TextNode(item[2:], TextType.TEXT)])
                    for element in test :
                        if element.text_type == TextType.TEXT:
                            node_child.children.append(LeafNode(None, element.text))
                        elif element.text_type == TextType.BOLD:
                            node_child.children.append(LeafNode("b", element.text))
                        elif element.text_type == TextType.ITALIC:
                            node_child.children.append(LeafNode("i", element.text))
                        elif element.text_type == TextType.IMAGE:
                            node_child.children.append(LeafNode("img", "", {"src": element.url,"alt": element.text}))
                        elif element.text_type == TextType.LINKS:  
                            node_child.children.append(LeafNode("a", element.text, {"href": element.url}))
                        elif element.text_type == TextType.CODE:
                            node_child.children.append(LeafNode("code", element.text))
                    children.append(node_child)
            node = ParentNode("ul", children)
        elif block_type == BlockType.ORDERED:
            items = block.split("\n")
            children = []
            for item in items:
                if item[0].isdigit() and item[1] == ".":
                    node_child = ParentNode("li",[])
                    test = text_to_textnodes([TextNode(item[3:], TextType.TEXT)])
                    for element in test :
                        if element.text_type == TextType.TEXT:
                            node_child.children.append(LeafNode(None, element.text))
                        elif element.text_type == TextType.BOLD:
                            node_child.children.append(LeafNode("b", element.text))
                        elif element.text_type == TextType.ITALIC:
                            node_child.children.append(LeafNode("i", element.text))
                        elif element.text_type == TextType.IMAGE:
                            node_child.children.append(LeafNode("img", "", {"src": element.url,"alt": element.text}))
                        elif element.text_type == TextType.LINKS:  
                            node_child.children.append(LeafNode("a", element.text, {"href": element.url}))
                        elif element.text_type == TextType.CODE:
                            node_child.children.append(LeafNode("code", element.text))
                    children.append(node_child)
            node = ParentNode("ol", children)
        elif block_type == BlockType.CODE:
            code = block[3:-3].strip()
            node = ParentNode("pre", [LeafNode("code", code)])
        else :
            node = ParentNode("p",[])
            test = text_to_textnodes([TextNode(block, TextType.TEXT)])
            for element in test :
                if element.text_type == TextType.TEXT:
                    node.children.append(LeafNode(None, element.text))
                elif element.text_type == TextType.BOLD:
                    node.children.append(LeafNode("b", element.text))
                elif element.text_type == TextType.ITALIC:
                    node.children.append(LeafNode("i", element.text))
                elif element.text_type == TextType.IMAGE:
                    node.children.append(LeafNode("img", element.text, {"src": element.url}))
                elif element.text_type == TextType.LINKS:  
                    node.children.append(LeafNode("a", element.text, {"href": element.url}))
                elif element.text_type == TextType.CODE:
                    node.children.append(LeafNode("code", element.text))
        nodes.append(node)
    return ParentNode("body", nodes)

def copy_directory_recursively(src, dst):
    import shutil
    import os
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    os.listdir(src)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory_recursively(s, d)
        else:
            shutil.copy2(s, d)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in the markdown")

def generate_page(from_path, template_path,dest_path):
    print("Generating page...")
    with open(from_path, "r") as f:
        markdown = f.read()
    title = extract_title(markdown)
    with open(template_path, "r") as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_node.to_html())
    with open(dest_path, "w") as f:
        f.write(html)

def generate_page_recursively(from_path, template_path,dest_path):
    import os
    import shutil
    print("Generating page recursively...")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    for item in os.listdir(from_path):
        s = os.path.join(from_path, item)
        d = os.path.join(dest_path, item)
        if os.path.isdir(s):
            generate_page_recursively(s, template_path, d)
        else:
            if item.endswith(".md"):
                generate_page(s, template_path, d.replace(".md", ".html"))
            else:
                shutil.copy2(s, d)
def main():
    copy_directory_recursively("static", "public")
    generate_page_recursively("content/", "template.html", "public/")

main()