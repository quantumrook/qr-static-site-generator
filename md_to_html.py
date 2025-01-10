from private import base_path, templates

from handlers.frontmatter import handle_frontmatter
from handlers.callout import handle_callouts
from handlers.headers import handle_headers
from handlers.merge_with_post import merge_with_post
from handlers.styling import handle_styling
from handlers.lists import handle_lists

markdown_to_convert_fp = f"{base_path}\\templates\\example.md"
markdown_to_convert_lines = [ ]

with open(markdown_to_convert_fp, "r") as file:
    markdown_to_convert_lines = file.readlines()

# Get frontmatter
title, date_created, dates_modified, markdown_body = handle_frontmatter(markdown_to_convert_lines)
frontmatter = (title, date_created, dates_modified[-1])

# Handle callouts
markdown_body = handle_callouts(markdown_body)
    
# Handle styling (like bold, italics, etc)
markdown_body = handle_styling(markdown_body)

# Handle lists
markdown_body = handle_lists(markdown_body)

# Handle headers
markdown_body = handle_headers(markdown_body)

# Replace template with content

## Replace Post Template with content
squished_post = merge_with_post(markdown_body, frontmatter)

## Replace Base template with post

base_fp = f"{base_path}{templates["base"]}"
base_html_template = [ ]

with open(base_fp, "r") as file:
    base_html_template = file.readlines()

for i, line in enumerate(base_html_template):
    if "{{title}}" in line:
        base_html_template[i] = line.replace("{{title}}", title)
    if "{{body}}" in line:
        base_html_template[i] = line.replace("{{body}}", squished_post)

new_html = f"{base_path}\\content\\{title}.html"

with open(new_html, "w+") as file:
    file.writelines(base_html_template)