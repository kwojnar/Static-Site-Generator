from enum import Enum
import re


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
                )
                
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("Invalid Markdown. formatted section not closed")
        for index in range(len(split_node)):
            if split_node[index] == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(split_node[index], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(split_node[index], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        text = node.text
        regex = r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))"
        link_indexes = []
        all_indexes = []
        for match in re.finditer(regex, text):
            link_indexes.append((match.start(), match.end(), TextType.LINK))
        if not link_indexes:
            new_nodes.append(node)
            continue
        for link_index in link_indexes:
            if link_index[0] > 0 and not all_indexes:
                new_nodes.append(TextNode(text[0:link_index[0]], TextType.NORMAL))
                all_indexes.append((0, link_index[0], TextType.NORMAL))
            if len(all_indexes) > 0:
                if all_indexes[-1][1] < link_index[0]:
                    new_nodes.append(TextNode(text[all_indexes[-1][1]:link_index[0]], TextType.NORMAL))
                    all_indexes.append((all_indexes[-1][1], link_index[0], TextType.NORMAL))
            link_tuple = extract_markdown_links(text[link_index[0]:link_index[1]])[0]
            new_nodes.append(TextNode(link_tuple[0], link_index[2], link_tuple[1]))
            all_indexes.append(link_index)
        else:
            if all_indexes[-1][1] != len(text):
                new_nodes.append(TextNode(text[all_indexes[-1][1]:], TextType.NORMAL))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        text = node.text
        regex = r"(!\[[^\[\]]*\]\([^\(\)]*\))"
        image_indexes = []
        all_indexes = []
        for match in re.finditer(regex, text):
            image_indexes.append((match.start(), match.end(), TextType.IMAGE))
        if not image_indexes:
            new_nodes.append(node)
            continue
        for image_index in image_indexes:
            if image_index[0] > 0 and not all_indexes:
                new_nodes.append(TextNode(text[0:image_index[0]], TextType.NORMAL))
                all_indexes.append((0, image_index[0], TextType.NORMAL))
            if len(all_indexes) > 0:
                if all_indexes[-1][1] < image_index[0]:
                    new_nodes.append(TextNode(text[all_indexes[-1][1]:image_index[0]], TextType.NORMAL))
                    all_indexes.append((all_indexes[-1][1], image_index[0], TextType.NORMAL))
            image_tuple = extract_markdown_images(text[image_index[0]:image_index[1]])[0]
            new_nodes.append(TextNode(image_tuple[0], image_index[2], image_tuple[1]))
            all_indexes.append(image_index)
        else:
            if all_indexes[-1][1] != len(text):
                new_nodes.append(TextNode(text[all_indexes[-1][1]:], TextType.NORMAL))
    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.NORMAL)
    nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
