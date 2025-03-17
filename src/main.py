from textnode import TextNode, TextType

import sys

from path_utilites import copy_contents, generate_page, generate_pages_recursive

def main():
    copy_contents('static', 'docs')
    # generate_page('content/index.md', 'template.html', 'public/index.html')
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(basepath)
    generate_pages_recursive('content', 'template.html', 'docs', basepath )


main()