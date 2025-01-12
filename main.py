from typing import Any
from private import base_path

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
        print("")
    print("")

print("\n")
rough_blocks = get_rough_blocks_of_content(f"{base_path}\\raw\\example.md")
grouped_by_headers = group_blocks_by_header(rough_blocks)
nested_content = nest_subheadings_inside_headings(grouped_by_headers)
print_nested(nested_content)

def format_content(nested_blocks_of_content):
    html_content = [ ]
    for h2, h2_content in nested_blocks_of_content.items():
        for h3, h3_content in h2_content.items():
            #if h3 == "content":
                
            for h4, h4_content in h3_content.items():
                for h5, h5_content in h4_content.items():
                    for h6, h6_content in h5_content.items():
                        format_block(h6, h6_content)

def format_block(header: str, block_of_content):
    formatted_block = ""
    header_level = header.count("#")
    header = header.strip("#").strip(" ")
    header_id = "-".join(header.split(" "))
    block_prefix = f'<section class=h{header_level}><h{header_level} id="{header_id}">{header}</h{header_level}>'
    block_suffix = f'</section>'
    
    # for sub_block in block_of_content:
        
    print(block_prefix)
    return formatted_block

format_block("#### With its own H4", "")