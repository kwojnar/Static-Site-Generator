import re

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
    