from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown : str):
    return list(filter(lambda x : x != "", list(map(lambda x : x.strip(), markdown.split("\n\n")))))

def block_to_block_type(block: str):
    lines = block.split("\n")
    if re.search(r"^#{1,6}\s.+", block):
        return BlockType.HEADING
    
    if re.search(r"^`{3}", lines[0]) and re.search(r"^`{3}", lines[-1]):
        return BlockType.CODE
    
    if re.search(r"^>", block):
        for line in lines:
            if not re.search(r"^>", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if re.search(r"^-\s", block):
        for line in lines:
            if not re.search(r"^-\s", line):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if re.search(r"^1\.\s", block):
        for i in range(len(lines)):
            if not re.search(fr"^{i+1}\.\s", lines[i]):
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    div_node = ParentNode('div', [])
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = create_html_node(block_type, block)
        div_node.children.append(block_node)

    return div_node

    



def create_html_node(block_type: BlockType, block: str):
    match block_type:
        case BlockType.HEADING:
            pound_count = block.count("#")
            if pound_count + 1 >= len(block):
                raise ValueError(f"invalid heading level: {level}")
            child_nodes = text_to_children(block[pound_count+1 :])
            return  ParentNode(f"h{pound_count}", child_nodes)
        case BlockType.CODE:
            code_text = text_node_to_html_node(TextNode(block[4:-3].strip("\n"), TextType.CODE))
            return ParentNode('pre', [code_text])
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            child_nodes=text_to_children(paragraph)
            return ParentNode('p', child_nodes)
        case BlockType.QUOTE:
            lines = block.replace(">","").split("\n")
            blockquote = "".join(lines)
            child_nodes = text_to_children(blockquote)
            return ParentNode('blockquote', child_nodes)
        case BlockType.ULIST:
            lines = block.split("\n")
            child_nodes = list(map(lambda x: ParentNode("li", text_to_children(x[2:])), lines))
            return ParentNode('ul', child_nodes)
        case BlockType.OLIST:
            lines = block.split("\n")
            child_nodes = list(map(lambda x: ParentNode("li", text_to_children(x[3:])), lines))
            return ParentNode('ol', child_nodes)

def text_to_children(str):
    return list(map(lambda x : text_node_to_html_node(x), text_to_textnodes(str.strip())))


def extract_title(markdown: str):
    header = markdown.split("\n")[0].replace("# ", "").strip()
    if header.count("#") != 0:
        raise Exception("No title ( h1 )")
    return header

# def extract_content(markdown: str):
#     return "\n\n".join(markdown.split("\n\n")[1:])