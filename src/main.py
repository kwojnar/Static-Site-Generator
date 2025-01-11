from textnode import *
from htmlnode import *
from block_markdown import *
import re


def main():
    text = "Rummy"
    text_type = TextType.NORMAL
    url = "urly://url.url"

    dummy = TextNode(text, text_type, url)
    print(dummy)


if __name__ == "__main__":
    main()

