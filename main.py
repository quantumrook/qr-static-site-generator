from private import base_path, templates

import os

from chunk_markdown import chunk_markdown_file, print_nested

from handlers.frontmatter import handle_frontmatter
from handlers.callout import handle_callouts
from handlers.merge_with_post import merge_with_post
from handlers.lists import handle_lists
from handlers.links import handle_links
from handlers.preformatted import handle_preformatted_blocks
from handlers.tables import handle_tables
from handlers.regex import convert_formatting

def format_content(nested_blocks_of_content):
    html_content = ""
    for h2, h2_content in nested_blocks_of_content.items():
        h2_prefix, h2_indent, h2_suffix = get_block_wrapper(h2)
        h2_block = ""
        for h3, h3_content in h2_content.items():
            if h3 == "content":
                h2_block += format_block(h2_indent, h3_content)
            else:
                h3_prefix, h3_indent, h3_suffix = get_block_wrapper(h3)
                h3_block = ""
                for h4, h4_content in h3_content.items():
                    if h4 == "content":
                        h3_block += format_block(h3_indent, h4_content)
                    else:
                        h4_prefix, h4_indent, h4_suffix = get_block_wrapper(h4)
                        h4_block = ""
                        for h5, h5_content in h4_content.items():
                            if h5 == "content":
                                h4_block += format_block(h4_indent, h5_content)
                            else:
                                h5_prefix, h5_indent, h5_suffix = get_block_wrapper(h5)
                                h5_block = ""
                                for h6, h6_content in h5_content.items():
                                    if h6 == "content":
                                        h5_block += format_block(h5_indent, h6_content)
                                    else:
                                        h6_prefix, h6_indent, h6_suffix = get_block_wrapper(h6)
                                        h6_block = ""
                                        for sub_h6, sub_h6_content in h6_content.items():
                                            h6_block += format_block(h6_indent, sub_h6_content)
                                        h5_block += h6_prefix + h6_block + h6_suffix
                                h4_block += h5_prefix + h5_block + h5_suffix
                        h3_block += h4_prefix + h4_block + h4_suffix
                h2_block += h3_prefix + h3_block + h3_suffix
        html_content += h2_prefix + h2_block + h2_suffix

    return html_content

def get_block_wrapper(header):
    header_level = header.count("#")
    
    indent_level = ""
    for i in range(0, header_level):
        indent_level += "\t"
    header = header.strip("#").strip(" ")
    header_id = "-".join(header.split(" "))
    block_prefix = f'{indent_level}<section class=h{header_level}><h{header_level} id="{header_id}">{header}</h{header_level}>\n'
    block_suffix = f'{indent_level}</section>\n'
    
    return (block_prefix, indent_level, block_suffix)

def format_block(indent_level, block_of_content):
    formatted_block = ""
    block = ""
    indent_level += "\t"

    for sub_block in block_of_content:
        sub_block = handle_tables(sub_block)
        sub_block = handle_callouts(sub_block)
        sub_block = handle_links(sub_block)
        sub_block = convert_formatting(sub_block)
        sub_block = handle_lists(sub_block)
        sub_block = handle_preformatted_blocks(sub_block)
        for line in sub_block:
            for sub_line in line.split("\n"):
                block += indent_level + sub_line + "\n"
        block += indent_level + "<br />\n"
    
    formatted_block = block 
    return formatted_block


def load_files(source_directory: str, destination_directory: str, fresh_build:bool = False):
    files_to_convert = { }
    files_in_source = os.listdir(source_directory)
    
    if fresh_build:
        for file in files_in_source:
            if file.endswith(".md"):
                with open(source_directory + file, "r") as reader:
                    files_to_convert[file] = reader.readlines()
        return files_to_convert
    
    # Not a fresh build, we only want to convert what has changed
    files_in_destination = os.listdir(destination_directory)
    for src_file in files_in_source:
        if not src_file.endswith(".md"): #skip anything that's not markdown
            continue
        for dest_file in files_in_destination:
            if not dest_file.endswith(".html"): #skip anything thats not html
                continue
            if src_file.strip(".md").lower() == dest_file.strip(".html").lower():
                src_last_modified = os.path.getmtime(source_directory + src_file)
                dest_last_modified = os.path.getmtime(destination_directory + dest_file)
                if src_last_modified <= dest_last_modified:
                    continue
        with open(source_directory + src_file, "r") as reader:
            files_to_convert[src_file] = reader.readlines()
    return files_to_convert


def old_core_loop(nested_content):
    html_string = format_content(nested_content)

    title = "raw"

    # with open(f"{base_path}\\raw.html", "w+") as file:
    #     file.write(html_string)
        
    base_fp = f"{base_path}{templates["base"]}"
    base_html_template = [ ]

    with open(base_fp, "r") as file:
        base_html_template = file.readlines()

    for i, line in enumerate(base_html_template):
        if "{{title}}" in line:
            base_html_template[i] = line.replace("{{title}}", title)
        if "{{body}}" in line:
            base_html_template[i] = line.replace("{{body}}", html_string)

    new_html = f"{base_path}\\content\\{title}.html"

    with open(new_html, "w+") as file:
        file.writelines(base_html_template)


def main():
    files = load_files(f"{base_path}\\raw\\", f"{base_path}\\content\\", False)

    for fname, content in files.items():
            # Get frontmatter
        title, date_created, dates_modified, markdown_body = handle_frontmatter(content)
        frontmatter = (title, date_created, dates_modified[-1])
        chunked_content = chunk_markdown_file(markdown_body)
        files[fname] = {
            "frontmatter" : frontmatter,
            "content"     : chunked_content
        }
    # Handle embedded stuff
    
    # Finish conversion and make output file
    for fname in list(files.keys()):
        frontmatter = files[fname]["frontmatter"]
        body_content = files[fname]["content"]
        
        formatted_content = format_content(body_content)
        
        squished_post = merge_with_post(formatted_content, frontmatter)
        
        base_fp = f"{base_path}{templates["base"]}"
        base_html_template = [ ]

        with open(base_fp, "r") as file:
            base_html_template = file.readlines()

        for i, line in enumerate(base_html_template):
            if "{{title}}" in line:
                base_html_template[i] = line.replace("{{title}}", frontmatter[0])
            if "{{body}}" in line:
                base_html_template[i] = line.replace("{{body}}", squished_post)

        new_html = f"{base_path}\\content\\{frontmatter[0]}.html"

        with open(new_html, "w+") as file:
            file.writelines(base_html_template)
        
if __name__ == "__main__":
    main()