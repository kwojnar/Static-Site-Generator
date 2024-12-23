import textnode

def main():
    text = "Rummy"
    text_type = textnode.TextType.NORMAL_TYPE
    url = "urly://url.url"

    dummy = textnode.TextNode(text, text_type, url)
    print(dummy)

if __name__ == "__main__":
    main()

