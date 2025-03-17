import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image_or_link, text_to_textnodes
from textnode import TextNode, TextType, TextTypeDelimiter



class TestInlineMD(unittest.TestCase):
    def test_single_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextTypeDelimiter.CODE.value , TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_on_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    
    # def test_split_images(self):
    #     node = TextNode(
    #         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_image_or_link([node], TextType.IMAGE)
    #     self.assertListEqual(
    #         [
    #             TextNode("This is text with an ", TextType.TEXT),
    #             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
    #             TextNode(" and another ", TextType.TEXT),
    #             TextNode(
    #                 "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
    #             )
    #         ],
    #         new_nodes,
    #     )
    
    # def test_split_links(self):
    #     node = TextNode(
    #         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_image_or_link([node], TextType.LINK)
    #     self.assertListEqual(
    #          [
    #             TextNode("This is text with a link ", TextType.TEXT),
    #             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #             TextNode(" and ", TextType.TEXT),
    #             TextNode(
    #                 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
    #             ),
    #         ],
    #         new_nodes,
    #     )
    
    # def test_split_image(self):
    #     node = TextNode(
    #         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_image_or_link([node], TextType.IMAGE)
    #     self.assertListEqual(
    #         [
    #             TextNode("This is text with an ", TextType.TEXT),
    #             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
    #         ],
    #         new_nodes,
    #     )

    # def test_split_image_single(self):
    #     node = TextNode(
    #         "![image](https://www.example.COM/IMAGE.PNG)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_image_or_link([node], TextType.IMAGE)
    #     self.assertListEqual(
    #         [
    #             TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
    #         ],
    #         new_nodes,
    #     )
    
    def test_split_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()