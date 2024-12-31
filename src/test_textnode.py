import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_italic(self):
        test_case = split_nodes_delimiter([TextNode("Normal *Italic* Another Normal", TextType.NORMAL)], "*", TextType.ITALIC)
        expected_result = [
                TextNode("Normal ", TextType.NORMAL),
                TextNode("Italic", TextType.ITALIC),
                TextNode(" Another Normal", TextType.NORMAL)
                ]
        self.assertEqual(test_case, expected_result)


    def test_multiple_italic(self):
        test_case = split_nodes_delimiter([TextNode("Normal *Italic* *Another Italic*", TextType.NORMAL)], "*", TextType.ITALIC)
        expected_result = [
                TextNode("Normal ", TextType.NORMAL),
                TextNode("Italic", TextType.ITALIC),
                TextNode("Another Italic", TextType.ITALIC)
                ]
    
    def test_bold(self):
        test_case = split_nodes_delimiter([TextNode("Normal **Bold** Another Normal", TextType.NORMAL)], "**", TextType.BOLD)
        expected_result = [
                TextNode("Normal ", TextType.NORMAL),
                TextNode("Bold", TextType.BOLD),
                TextNode(" Another Normal", TextType.NORMAL)
                ]
        self.assertEqual(test_case, expected_result)
    

    def test_code(self):
        test_case = split_nodes_delimiter([TextNode("`Code` Normal", TextType.NORMAL)], "`", TextType.CODE)
        expected_result = [
                TextNode("Code", TextType.CODE),
                TextNode(" Normal", TextType.NORMAL)
                ]
        self.assertEqual(test_case, expected_result)


    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        test_case = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_case = split_nodes_delimiter(test_case, "*", TextType.ITALIC)
        expected_result = [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ]
        self.assertEqual(test_case, expected_result)

if __name__ == "__main__":
    unittest.main()
