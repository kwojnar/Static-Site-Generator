from enum import Enum

class TextType(Enum):
    NORMAL_TYPE = "normal"
    BOLD_TYPE = "bold"
    ITALIC_TYPE = "italic"
    CODE_TYPE = "code"
    LINK_TYPE = "link"
    IMAGE_TYPE = "image"


class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        if text_type == TextType.LINK_TYPE or text_type == TextType.IMAGE_TYPE:
            self.url = None
        else:
            self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

