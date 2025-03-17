from textnode import TextNode, TextType

import sys

from path_utilites import copy_contents, generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_contents('static', 'docs')
    print(basepath)
    generate_pages_recursive('content', 'template.html', 'docs', basepath )


main()