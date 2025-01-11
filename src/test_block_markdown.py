import unittest

from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_basic(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected_result = [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        test_case = markdown_to_blocks(markdown)
        self.assertEqual(test_case, expected_result)

    def test_randomlinebreaksandwhitespaces(self):
        markdown = """
# This is a heading  

This is a paragraph of text. It has some **bold** and *italic* words inside of it.   

  * This is the first list item in a list block
* This is a list item
* This is another list item  
"""
        expected_result = [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        test_case = markdown_to_blocks(markdown)
        self.assertEqual(test_case, expected_result)

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

class TestBlockMarkdownType(unittest.TestCase):
    def test_heading(self):
        markdown = "# This is a heading"
        expected_result = "heading"
        test_case = block_to_block_type(markdown)
        self.assertEqual(test_case, expected_result)

    def test_quote(self):
        markdown = """> This is first line of quote
>This is second line of quote"""
        expected_result = "quote"
        test_case = block_to_block_type(markdown)
        self.assertEqual(test_case, expected_result)

    def test_code(self):
        markdown = """```
        #This is first line of code
        #This is second line of code
        ```"""
        expected_result = "code"
        test_case = block_to_block_type(markdown)
        self.assertEqual(test_case, expected_result)

    def test_unordered_list(self):
        markdown = """* first itme
- second item
- third item"""
        expected_result = "unordered_list"
        test_case = block_to_block_type(markdown)
        self.assertEqual(test_case, expected_result)

    def test_ordered_list(self):
        markdown = """1. first item
2. second item
3. third item"""
        expected_result = "ordered_list"
        test_case = block_to_block_type(markdown)
        self.assertEqual(test_case, expected_result)


class TestMarkdownToHTML(unittest.TestCase):
    def test_print(self):
        markdown = """
# This is a heading

## This is also a heading

####### This is not a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. lorem **bold lorem**
2. ipsum *italic lorem*
3. costam

> yolo

> ora
> **et**
> *labora*

```
nikczemnik
 ** gruby nikczemnik**
```
"""
        html_node = makrdown_to_html_node(markdown)
        expected_result = """<div><h2>This is a heading</h2><h3>This is also a heading</h3><p>####### This is not a heading</p><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><ol><li>lorem <b>bold lorem</b></li><li>ipsum <i>italic lorem</i></li><li>costam</li></ol><quote>yolo</quote><quote>ora
<b>et</b>
<i>labora</i></quote><code>
nikczemnik
 <b> gruby nikczemnik</b>
</code></div>"""
        self.assertEqual(html_node.to_html(), expected_result)