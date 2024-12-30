import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode("p",
                          [
                              LeafNode("b", "BOLD"),
                              LeafNode("i", "ITALIC")
                              ],
                          )
        self.assertEqual(node.to_html(), "<p><b>BOLD</b><i>ITALIC</i></p>")



    def test_eq2(self):
        node = ParentNode("p",
                          [
                              LeafNode("b", "BOLD"),
                              LeafNode("i", "ITALIC")
                              ],
                          {"href": "https://test.test"})
        self.assertEqual(node.to_html(), '<p href="https://test.test"><b>BOLD</b><i>ITALIC</i></p>')
    
    def test_eq3(self):
        node = ParentNode("p",
                          [
                              ParentNode("p",
                            [
                                LeafNode("b", "BOLD"),
                                LeafNode("i", "ITALIC")
                                ]),
                            LeafNode("b", "ANOTHER BOLD")
                            ],
                          {"href": "https://test.test"})
        self.assertEqual(node.to_html(), '<p href="https://test.test"><p><b>BOLD</b><i>ITALIC</i></p><b>ANOTHER BOLD</b></p>')

    def test_noChildren(self):
        node = ParentNode("p", [])
        self.assertRaises(Exception, node.to_html, None)

if __name__ == "__main__":
    unittest.main()
