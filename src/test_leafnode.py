import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "value of tag1")
        node2 = LeafNode("p", "value of tag1")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = LeafNode("a", "value of tag1", props={})
        node2 = LeafNode("a", "value of tag1", props={})
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = LeafNode("h1", "value of tag1")
        node2 = LeafNode("h2", "value of tag1")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = LeafNode("p", "value", {"href": "https://test.test"})
        self.assertEqual(node.to_html(), '<p href="https://test.test">value</p>')


if __name__ == "__main__":
    unittest.main()
