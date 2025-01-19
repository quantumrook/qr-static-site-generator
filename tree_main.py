
from typing import Any

from private import raw, base_path
from handlers.reader import get_files
from handlers.chopper import chop
from handlers.formatter import handle_formatting
from handlers.writer import write_files
from handlers.embedder import get_embedding_info, embed

def convert_files_to_nodes(files: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """_summary_

    Args:
        files (dict[str, dict[str, Any]]): _description_

    Returns:
        dict[str, dict[str, Any]]: _description_
    """
    filenames = list(files.keys())
    for filename in filenames:
        lines = files[filename]["content"]
        frontmatter, body_node = chop(lines)
        files[filename]["frontmatter"] = frontmatter
        files[filename]["content"] = body_node

    return files

def main(source_directory: str, destination_directory: str):
    """_summary_

    Args:
        source_directory (str): _description_
        destination_directory (str): _description_
    """
    files = get_files(source_directory, destination_directory, fresh_build=True)
    files = convert_files_to_nodes(files)

    filenames = list(files.keys())
    for filename in filenames:
        files[filename]["content"] = handle_formatting(files[filename]["content"])
        files[filename]["embeds"] = get_embedding_info(files[filename]["content"])
    files = embed(files)
    write_files(files, destination_directory)

if __name__ == "__main__":

    main(
        raw["directory"],
        f'{base_path}\\tests\\'
    )
