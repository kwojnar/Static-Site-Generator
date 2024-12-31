from enum import Enum

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
