import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is an italic node", TextType.ITALIC, url=None)
        node2 = TextNode("This is an italic node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is an italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is random", TextType.BOLD, "urly://url.url")
        node2 = TextNode("This is not random", TextType.BOLD, "urly://url.url")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()