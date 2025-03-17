import os
import shutil

from block_markdown import extract_title, markdown_to_html_node

def copy_contents(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if os.path.exists(src):
        os.mkdir(os.path.join(os.getcwd(),dest))

        for item in os.listdir(src):
            item_src = os.path.join(src, item)
            item_dest = os.path.join(dest, item)
            if os.path.isdir(item_src):
                copy_contents(item_src, item_dest)
            else:
                shutil.copy(item_src, item_dest)

    else:
        raise Exception("Not a valid path")

def generate_page(from_path, template_path, dest_path, basepath ):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_content = ""
    template_content = ""
    with open(from_path, "r") as file:
        from_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    
    extracted_html = markdown_to_html_node(from_content).to_html()
    extracted_title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", extracted_title).replace("{{ Content }}", extracted_html).replace('href="/', f'href="/{basepath}').replace('src="/', f'src="/{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath ):
    if os.path.exists(dir_path_content):
        for item in os.listdir(dir_path_content):
            item_src = os.path.join(dir_path_content, item)
            item_dest = os.path.join(dest_dir_path, item).replace(".md", ".html")
            if os.path.isdir(item_src):
                generate_pages_recursive(item_src,template_path, item_dest, basepath)
            else:
                generate_page(item_src, template_path, item_dest,basepath)