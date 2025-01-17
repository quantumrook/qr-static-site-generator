
from typing import Any
from markdown_node import MarkdownNode
from handlers.reader import get_files
from handlers.chopper import chop

def convert_files_to_nodes(files: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    
    filenames = list(files.keys())
    for filename in filenames:
        lines = files[filename]["content"]
        frontmatter, body_node = chop(lines)
        files[filename]["frontmatter"] = frontmatter
        files[filename]["content"] = body_node

    return files

def main(source_directory, destination_directory):
    files = get_files(source_directory, destination_directory, fresh_build=True)
    files = convert_files_to_nodes(files)


if __name__ == "__main__":
    
    main()