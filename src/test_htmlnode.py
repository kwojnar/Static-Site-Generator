import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "value of tag1")
        node2 = HTMLNode("p", "value of tag1")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("a", "value of tag1", children=None, props={})
        node2 = HTMLNode("a", "value of tag1", props={})
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("h1", "value of tag1")
        node2 = HTMLNode("h2", "value of tag1")
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = HTMLNode(children=[])
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
