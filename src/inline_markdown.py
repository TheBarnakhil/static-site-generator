from typing import List
import re

from textnode import TextNode, TextType, TextTypeDelimiter

'''
    This function is responsible for splitting "text" type text nodes into smaller chunks based on the delimiter provided and the target text type.
'''
def split_nodes_delimiter(old_nodes : List[TextNode], delimiter : TextTypeDelimiter, text_type : TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node_text = node.text.split(delimiter)
            if len(split_node_text) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            for i in range(len(split_node_text)):
                if split_node_text[i] == "":
                    continue
                if i%2 == 0:
                    new_nodes.append(TextNode(split_node_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_node_text[i], text_type=text_type))
    
    return new_nodes



'''
This function behaves very similarly to split_nodes_delimiter, but doesn't need a delimiter,takes text_type to distinguish between images and links
'''
def split_nodes_image_or_link(old_nodes : List[TextNode], text_type : TextType):
    new_nodes = []
    for node in old_nodes:
        if len(node.text) == 0:
            continue
        
        extracted_md = extract_markdown_images(node.text) if text_type == TextType.IMAGE else extract_markdown_links(node.text)
        
        if len(extracted_md) == 0:
            new_nodes.append(node)
        else:
            sections = []
            for ext in extracted_md:
                delimiter = f"{"!" if text_type == TextType.IMAGE else ""}[{ext[0]}]({ext[1]})" 
                if len(sections)==0 :
                    sections.extend(convert_to_node(node.text.split(delimiter, 1) , ext, text_type))
                else:
                    section_to_split = sections.pop()
                    sections.extend(convert_to_node(section_to_split.split(delimiter, 1) , ext, text_type))
            if not isinstance(sections[-1], TextNode):
                sections[-1] = TextNode(sections[-1], TextType.TEXT)
            new_nodes.extend(sections)
    
    return new_nodes


def text_to_textnodes(text) -> List[TextNode]:
    node = TextNode(text,TextType.TEXT)
    new_nodes_list = []
    new_nodes_list = split_nodes_delimiter([node], TextTypeDelimiter.BOLD.value, TextType.BOLD)
    new_nodes_list = split_nodes_delimiter(new_nodes_list, TextTypeDelimiter.CODE.value, TextType.CODE)
    new_nodes_list = split_nodes_delimiter(new_nodes_list, TextTypeDelimiter.ITALIC.value, TextType.ITALIC)
    new_nodes_list = split_nodes_image_or_link(new_nodes_list, TextType.IMAGE)
    new_nodes_list = split_nodes_image_or_link(new_nodes_list, TextType.LINK)
    return new_nodes_list



'''
    This function takes raw markdown text and returns a list of tuples.
    Each tuple will contain the alt text and the URL of any markdown images
'''
def extract_markdown_images(text):
    values = re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return values

'''
    This function takes raw markdown text and returns a list of tuples.
    Each tuple will contain the alt text and the URL of any markdown links
'''
def extract_markdown_links(text):
    values = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return values




'''
Helper
'''
def convert_to_node(arr, ext, text_type) :
    new_arr = []
    if len(arr) != 2:
        raise ValueError("invalid markdown, image section not closed")
    if arr[0] != "":
        new_arr.append(TextNode(arr[0], TextType.TEXT))
    
    new_arr.append(TextNode(ext[0], text_type, ext[1] ))

    if len(arr) == 2 and arr[1] != '':
        new_arr.append(arr[1])
    return new_arr