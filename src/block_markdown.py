import re

from htmlnode import ParentNode
from textnode import text_to_html_nodes

class BlockType:
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_ulist = "unordered_list"
    block_type_olist = "ordered_list"
    block_type_paragraph = "paragraph"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(None, blocks))
    return blocks

def block_to_block_type(markdown_block):
    heading_regex = r"^#{1,6}\s*\w"
    code_regex = r"^`{3}[^`]*`{3}$"
    quote_regex = r"^>.*"
    unordered_list_regex = r"^[*-]\s*"
    ordered_list_regex = r"^\d*[.]\s*"
    ordered_list__start_regex = r"^1*[.]\s*"
    if re.search(heading_regex, markdown_block):
        return BlockType.block_type_heading
    if re.search(code_regex, markdown_block):
        return BlockType.block_type_code
    if re.search(quote_regex, markdown_block):
        block_lines = markdown_block.split("\n")
        is_quote_block = True
        for block_line in block_lines:
            if not re.search(quote_regex, block_line):
                is_quote_block = False
        if is_quote_block:
            return BlockType.block_type_quote
    if re.search(unordered_list_regex, markdown_block):
        block_lines = markdown_block.split("\n")
        is_unordered_list_block = True
        for block_line in block_lines:
            if not re.search(unordered_list_regex, block_line):
                is_unordered_list_block = False
        if is_unordered_list_block:
            return BlockType.block_type_ulist
    if re.search(ordered_list__start_regex, markdown_block):
        block_lines = markdown_block.split("\n")
        is_ordered_list_block = True
        next_index = 1
        for block_line in block_lines:
            if not re.search(ordered_list_regex, block_line) or not block_line.startswith(str(next_index)):
                is_ordered_list_block = False
            next_index += 1
        if is_ordered_list_block:
            return BlockType.block_type_olist
    return BlockType.block_type_paragraph
    

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

def extract_title(markdown):
    lines = markdown.split()
    for line in lines:
        if line.startswith("# "):
            return line.rstrip("# ")
    raise Exception("Title header not found in provided markdown!")