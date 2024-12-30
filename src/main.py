from textnode import TextNode, TextType

def main():
    text = "Rummy"
    text_type = TextType.NORMAL
    url = "urly://url.url"

    dummy = TextNode(text, text_type, url)
    print(dummy)

if __name__ == "__main__":
    main()

