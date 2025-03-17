from textnode import TextNode, TextType

from path_utilites import copy_contents, generate_page, generate_pages_recursive

def main():
    copy_contents('static', 'public')
    # generate_page('content/index.md', 'template.html', 'public/index.html')
    generate_pages_recursive('content', 'template.html', 'public')


main()