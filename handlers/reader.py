import os
from typing import Any

def get_files(source_directory: str, destination_directory: str, fresh_build: bool = False) -> dict[str, list[str]]:

    source_files = read_source(source_directory)
    if not fresh_build:
        return source_files

    files_to_build = { }

    built_files = read_destination(destination_directory)
    destination_files = list(built_files.keys())
    for src_file in list(source_files.keys()):
        filename = src_file.strip(".md")
        src_modified = source_files[src_file]["modified"]
        if filename in destination_files:
            dest_modified = built_files[f"{filename}.html"]["modified"]
            if dest_modified < src_modified:
                files_to_build[src_file] = {"content" : source_files[src_file]["content"]}
        else:
            files_to_build[src_file] = {"content" : source_files[src_file]["content"]}
    return files_to_build

def read_source(source_directory: str) -> dict[str, Any]:
    files_to_convert = { }
    files_in_source = os.listdir(source_directory)
    
    for src_file in files_in_source:
        if src_file.endswith(".md"):
            files_to_convert[src_file] = { "modified" : os.path.getmtime(source_directory + src_file) }
            with open(source_directory + src_file, "r") as reader:
                files_to_convert[src_file]["content"] = reader.readlines()
    
    # TODO:: Handle nested directories
    
    return files_to_convert

def read_destination(destination_directory: str) -> dict[str, float]:
    already_built_files = { }
    files_in_destination = os.listdir(destination_directory)
    for dest_file in files_in_destination:
        if dest_file.endswith(".html"): #skip anything thats not html
            already_built_files[dest_file] = { "modified" : os.path.getmtime(destination_directory + dest_file)}

    return already_built_files
    