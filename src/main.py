from textnode import *
from htmlnode import *
from block_markdown import *
import re
import os
import shutil


def main():
    source_path = "/home/karol/Code/boot.dev/github/KWOJNAR/Static-Site-Generator/static"
    destination_path = "/home/karol/Code/boot.dev/github/KWOJNAR/Static-Site-Generator/public"
    update_destination_directory(source_path, destination_path)
    from_path = "/home/karol/Code/boot.dev/github/KWOJNAR/Static-Site-Generator/content/index.md"
    template_path = "/home/karol/Code/boot.dev/github/KWOJNAR/Static-Site-Generator/template.html"
    to_path = "/home/karol/Code/boot.dev/github/KWOJNAR/Static-Site-Generator/public/index.html"
    generate_page(from_path, template_path, to_path)

def copy_files_from_source(source_path, destination_path):
    files = os.listdir(source_path)
    for file in files:
        file_path = source_path + "/" + file
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination_path)
        else:
            new_destination_path = destination_path + "/" + file
            os.mkdir(new_destination_path)
            copy_files_from_source(file_path, new_destination_path)


def update_destination_directory(source_path, destination_path):
    if not os.path.exists(source_path):
        raise Exception(f"Source path does not exist: {source_path}")
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)
    else:        
        os.mkdir(destination_path)
    copy_files_from_source(source_path, destination_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    
    html_node = makrdown_to_html_node(markdown)
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_node.to_html())

    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    with open(dest_path, "w") as f: # to add directory check
        f.write(template)

if __name__ == "__main__":
    main()

