import unittest

from textnode import *

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


class TestExtractImagesAndLinks(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_case = extract_markdown_images(text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(test_case, expected_result)

    def test_extract_link(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_case = extract_markdown_links(text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(test_case, expected_result)

    def test_extract_link_and_image(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image_test = extract_markdown_images(text) 
        link_test = extract_markdown_links(text)
        test_case = link_test + image_test
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(test_case, expected_result)


class TestSplitNodesOnImagesAndLinks(unittest.TestCase):
    def test_extract_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )               
        test_case = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.NORMAL, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL, None),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(test_case, expected_result)
        
    def test_extract_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )               
        test_case = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.NORMAL, None),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL, None),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(test_case, expected_result)

    
    def test_extract_image_then_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )               
        test_case = split_nodes_image([node])
        test_case = split_nodes_link(test_case)
        expected_result = [
            TextNode("This is text with a link ", TextType.NORMAL, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL, None),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(test_case, expected_result)
    
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
