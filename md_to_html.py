from private import base_path, templates

from handlers.frontmatter import handle_frontmatter
from handlers.callout import handle_callouts
from handlers.headers import handle_headers
from handlers.merge_with_post import merge_with_post

markdown_to_convert_fp = f"{base_path}\\templates\\example.md"
markdown_to_convert_lines = [ ]

with open(markdown_to_convert_fp, "r") as file:
    markdown_to_convert_lines = file.readlines()
    
# Get frontmatter
title, date_created, dates_modified, markdown_body = handle_frontmatter(markdown_to_convert_lines)
frontmatter = (title, date_created, dates_modified[-1])

# Handle callouts
markdown_body = handle_callouts(markdown_body)
    
# Handle headers
markdown_body = handle_headers(markdown_body)

# squished_body = ""
# have_reached_text = False

# for line in markdown_body:
#     if line is "\n" and have_reached_text == False:
#         continue
#     else:
#         have_reached_text = True
#     if line is "\n":
#         squished_body += "<br />"
#     squished_body += line

base_fp = f"{base_path}{templates["base"]}"
base_html_template = [ ]

with open(base_fp, "r") as file:
    base_html_template = file.readlines()

# post_fp = f"{base_path}{templates["post"]}"
# post_html_template = [ ]

# with open(post_fp, "r") as file:
#     post_html_template = file.readlines()

# squished_post = ""
# for line in post_html_template:
#     if "{{frontmatter}}" in line:
#         last_modified = dates_modified[-1].strip("\n")
#         last_modified = last_modified.strip('"')
#         line = line.replace("{{frontmatter}}", f"Created: {date_created} <br/>Last Modified: {last_modified}")
#     if "{{post_body}}" in line:
#         line = line.replace("{{post_body}}", squished_body)

#     squished_post += line

squished_post = merge_with_post(markdown_body, frontmatter)

for i, line in enumerate(base_html_template):
    if "{{title}}" in line:
        base_html_template[i] = line.replace("{{title}}", title)
    if "{{body}}" in line:
        base_html_template[i] = line.replace("{{body}}", squished_post)

new_html = f"{base_path}\\content\\{title}.html"

with open(new_html, "w+") as file:
    file.writelines(base_html_template)