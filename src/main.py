from textnode import *
from htmlnode import *
from block_markdown import *
import re


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
        
def text_to_html_nodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes

def markdown_block_to_html_node(markdown_block, markdown_block_type):
    match markdown_block_type:
        case BlockType.block_type_heading:
            count = re.match(r"(^#*\s)", markdown_block).end()
            html_nodes = text_to_html_nodes(markdown_block[count:])
            return ParentNode(tag=f"h{count}", children=html_nodes)
        case BlockType.block_type_code:
            html_nodes = text_to_html_nodes(markdown_block.strip("```"))
            return ParentNode(tag="code", children=html_nodes)
        case BlockType.block_type_quote:
            quote_blocks = markdown_block.split("\n")
            quote_markdown_block = "\n".join(map(lambda line: line.lstrip("> "), quote_blocks))
            html_nodes = text_to_html_nodes(quote_markdown_block)
            return ParentNode(tag="quote", children=html_nodes)
        case BlockType.block_type_ulist:
            ulist_blocks = markdown_block.split("\n")
            ulist_blocks = list(map(lambda line: line[2:], ulist_blocks))
            ulist_html_nodes = list(map(lambda ulist_node: ParentNode(tag="li", children=text_to_html_nodes(ulist_node)), ulist_blocks))
            return ParentNode(tag="ul", children=ulist_html_nodes)
        case BlockType.block_type_olist:
            olist_blocks = markdown_block.split("\n")
            olist_blocks = (map(lambda line: re.match(r"(?:^\d*[.]\s)(.*)", line).group(1), olist_blocks))
            olist_html_nodes = list(map(lambda olist_node: ParentNode(tag="li", children=text_to_html_nodes(olist_node)), olist_blocks))
            return ParentNode(tag="ol", children=olist_html_nodes)
        case BlockType.block_type_paragraph:
            html_nodes = text_to_html_nodes(markdown_block)
            return ParentNode(tag="p", children=html_nodes)

def makrdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for markdown_block in markdown_blocks:
        markdown_block_type = block_to_block_type(markdown_block)
        children_nodes.append(markdown_block_to_html_node(markdown_block, markdown_block_type))
    return ParentNode(tag="div", children=children_nodes)


if __name__ == "__main__":
    main()

