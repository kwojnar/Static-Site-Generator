from textnode import TextNode, TextType
from htmlnode import LeafNode


def main():
    text = "Rummy"
    text_type = TextType.NORMAL
    url = "urly://url.url"

    dummy = TextNode(text, text_type, url)
    print(dummy)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Incorrect Text Type")

if __name__ == "__main__":
    main()

