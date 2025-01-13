from private import base_path, templates

from handlers.frontmatter import handle_frontmatter
from handlers.callout import handle_callouts
from handlers.merge_with_post import merge_with_post
from handlers.lists import handle_lists
from handlers.links import handle_links
from handlers.preformatted import handle_preformatted_blocks
from handlers.tables import handle_tables
from handlers.regex import convert_formatting

def get_rough_blocks_of_content(filepath: str) -> list[str]:

    with open(filepath, "r") as file:
        lines = file.readlines()

    last_line = len(lines) -1
        
    list_by_blocks_of_content = [ ]
    content_block = [ ]
    block_started = False
    for i, line in enumerate(lines):
        if line == "\n":
            if block_started:
                block_started = False
                list_by_blocks_of_content.append(content_block)
                
            if not block_started:
                block_started = True
                content_block = [ ]
        else:
            if block_started:
                content_block.append(line.strip('\n'))
        if i == last_line:
            list_by_blocks_of_content.append(content_block)

    return list_by_blocks_of_content

def group_blocks_by_header(rough_blocks: list[str]):
    headers = ['######', '#####', '####', '###', '##', '#']
    headers.reverse()
    grouped_by_headers = { }
    
    for header in headers:
        block_key = ""
        for block in rough_blocks:
            if header in block[0].split(" ")[0]:
                block_key = block[0]
                grouped_by_headers[block_key] = [ ]
            elif block_key:
                if block[0].split(" ")[0] not in headers:
                    grouped_by_headers[block_key].append(block)
                else:
                    block_key = ""
    
    return grouped_by_headers

def nest_subheadings_inside_headings(grouped_by_headers):
    headers = ['######', '#####', '####', '###', '##']
    headers.reverse()
    
    by_h2 = { }
    last_header = { }
    
    for header_key in list(grouped_by_headers.keys()):
        cleaned_key = header_key.split(" ")[0]
        last_header[cleaned_key] = header_key
        
        match cleaned_key:
            case "##":
                by_h2[header_key] = {"content" : grouped_by_headers[header_key]}
            case "###":
                by_h2[last_header["##"]][header_key] = {"content" : grouped_by_headers[header_key]}
            case "####":
                by_h2[last_header["##"]][last_header["###"]][header_key] = {"content" : grouped_by_headers[header_key]}
            case "#####":
                by_h2[last_header["##"]][last_header["###"]][last_header["####"]][header_key] = {"content" : grouped_by_headers[header_key]}
            case _:
                by_h2[last_header["##"]][last_header["###"]][last_header["####"]][last_header["#####"]][header_key] = {"content" : grouped_by_headers[header_key]} 
    
    return by_h2

def print_nested(by_h2):
    for h2, h2_content in by_h2.items():
        print(h2)
        for h3, h3_content in h2_content.items():
            print("  " + h3)
            if isinstance(h3_content, dict):
                for h4, h_4content in h3_content.items():
                    print("    "+h4)
                    print(f"      {h_4content}")
            else:
                for content in h3_content:
                    print(f"    {content}")

rough_blocks = get_rough_blocks_of_content(f"{base_path}\\raw\\example.md")
grouped_by_headers = group_blocks_by_header(rough_blocks)
nested_content = nest_subheadings_inside_headings(grouped_by_headers)
# print_nested(nested_content)

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
    indent_level = ""
    header = header.strip("#").strip(" ")
    header_id = "-".join(header.split(" "))
    block_prefix = f'{indent_level}<section class=h{header_level}><h{header_level} id="{header_id}">{header}</h{header_level}>\n'
    block_suffix = f'{indent_level}</section>\n'
    
    return (block_prefix, indent_level, block_suffix)

def format_block(indent_level, block_of_content):
    formatted_block = ""
    block = ""
    indent_level += "\t"
    indent_level = ""
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