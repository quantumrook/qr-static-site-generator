from private import base_path

import frontmatter_handler

templates = {
    "base" : "\\templates\\base.html",
    "post" : "\\templates\\post.html"
}

    
markdown_to_convert_fp = f"{base_path}\\templates\\example.md"
markdown_to_convert_lines = [ ]

with open(markdown_to_convert_fp, "r") as file:
    markdown_to_convert_lines = file.readlines()
    
# Get frontmatter

title, date_created, dates_modified, markdown_body = frontmatter_handler.handle_frontmatter(markdown_to_convert_lines)

# Handle callouts

callout_counter = 1
callout_indicies = [i for i, line in enumerate(markdown_body) if "> " in line]
previous_counter = 0
for i in callout_indicies:
    callout_content = markdown_body[i].strip("\n")
    if previous_counter == callout_counter:
        markdown_body[i] = callout_content.replace("> ", "<br/>\n")
    else:
        markdown_body[i] = callout_content.replace("> ", f'<div id="callout-{callout_counter}">')
        previous_counter = callout_counter
    if (i+1) not in callout_indicies:
        markdown_body[i] += "</div>\n"
        callout_counter += 1
    

# Handle headers

for j in range(6,0,-1):
    header_level = ""
    for k in range(j):
        header_level += "#"
    header_level += " "
    
    header_indicies = [i for i, line in enumerate(markdown_body) if header_level in line]
    for i in header_indicies:
        header_line = markdown_body[i].strip()
        markdown_body[i] = header_line.replace(header_level, f"<h{j}>") + f"</h{j}>\n"

squished_body = ""

for line in markdown_body:
    squished_body += line

base_fp = f"{base_path}{templates["base"]}"
base_html_template = [ ]

with open(base_fp, "r") as file:
    base_html_template = file.readlines()

post_fp = f"{base_path}{templates["post"]}"
post_html_template = [ ]

with open(post_fp, "r") as file:
    post_html_template = file.readlines()

squished_post = ""
for line in post_html_template:
    if "{{frontmatter}}" in line:
        last_modified = dates_modified[-1].strip("\n")
        last_modified = last_modified.strip('"')
        line = line.replace("{{frontmatter}}", f"Created: {date_created} <br/>Last Modified: {last_modified}")
    if "{{post_body}}" in line:
        line = line.replace("{{post_body}}", squished_body)

    squished_post += line

for i, line in enumerate(base_html_template):
    if "{{title}}" in line:
        base_html_template[i] = line.replace("{{title}}", title)
    if "{{body}}" in line:
        base_html_template[i] = line.replace("{{body}}", squished_post)

new_html = f"{base_path}\\content\\{title}.html"

with open(new_html, "w+") as file:
    file.writelines(base_html_template)