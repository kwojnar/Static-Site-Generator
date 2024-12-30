import unittest

from htmlnode import LeafNode
from textnode import TextType, TextNode
from main import text_node_to_html_node

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

if __name__ == "__main__":
    unittest.main()
