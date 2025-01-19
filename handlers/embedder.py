import re

from markdown_node import MarkdownNode


def get_embedding_info(article_node: MarkdownNode) -> list[tuple[str, int, str, str]]:
    embeddings = [ ]
    for branch in article_node.get_branch_name():
        content_block = article_node.get_content_for_branch_name(branch)

        if content_block is None:
            continue

        for index, line in enumerate(content_block):
            regex_match = re.search(r'!{1}\[{2}(?P<file_name>[^#]*)(?P<section_name>.*)\]{2}', line)

            if regex_match is not None:
                embeddings.append((branch, index, regex_match.group(1), regex_match.group(2)))
    return embeddings

def embed(files: dict) -> dict:
    filenames = list(files.keys())

    for filename in filenames:
        if files[filename]["embeds"]:
            root_node_destination = files[filename]["content"]
            embeddings = files[filename]["embeds"]
            for embedding in embeddings:
                branch_destination, index_destination, name_of_file_to_embed, name_of_section_to_embed = embedding
                name_of_file_to_embed += ".md"
                name_of_section_to_embed = name_of_section_to_embed.strip("#")
                if name_of_file_to_embed not in filenames:
                    print(f"Couldn't find {name_of_file_to_embed} for embedding into {filename}")
                    continue
                root_node_source = files[name_of_file_to_embed]["content"]
                for branch in root_node_source.get_branch_name():
                    if name_of_section_to_embed in branch:
                        name_of_section_to_embed = branch
                        break

                content_to_embed = root_node_source.get_content_for_branch_name(name_of_section_to_embed)
                string_to_embed = '<div class="callout-embed"><blockquote>' + "".join(content_to_embed) + "</blockquote></div>"
                destination_content = root_node_destination.get_content_for_branch_name(branch_destination)
                destination_content[index_destination] = re.sub(
                    r'!{1}\[{2}(?P<file_name>[^#]*)(?P<section_name>.*)\]{2}',
                    string_to_embed,
                    destination_content[index_destination]
                )
    return files
