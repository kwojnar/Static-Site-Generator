import unittest

from htmlnode import *
from textnode import *
from block_markdown import *
from main import *

class TestMain(unittest.TestCase):
    def test_text_to_html(self):
        text_node = TextNode("value of tag1", TextType.BOLD)
        converted_node = text_node_to_html_node(text_node)
        html_node = LeafNode("b", "value of tag1")
        self.assertEqual(converted_node, html_node)

    def test_noteq(self):
        text_node = TextNode("value of tag1", TextType.NORMAL)
        converted_node = text_node_to_html_node(text_node)
        html_node = LeafNode("b", "value of tag1")
        self.assertNotEqual(converted_node, html_node)

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

if __name__ == "__main__":
    unittest.main()
