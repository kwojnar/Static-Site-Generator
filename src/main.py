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
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    else:
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)
    copy_files_from_source(source_path, destination_path)



if __name__ == "__main__":
    main()

