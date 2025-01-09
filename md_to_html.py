from private import base_path

templates = {
    "base" : "\\templates\\base.html"
}

base_fp = f"{base_path}{templates["base"]}"
base_html_template = [ ]

with open(base_fp, "r") as file:
    base_html_template = file.readlines()
    
markdown_to_convert_fp = f"{base_path}\\templates\\example.md"
markdown_to_convert_lines = [ ]

with open(markdown_to_convert_fp, "r") as file:
    markdown_to_convert_lines = file.readlines()
    
# Get frontmatter

fm_start = markdown_to_convert_lines.index("---")
fm_end = markdown_to_convert_lines[1:].index("---")

title = ""
date_created = ""
dates_modified = [ ]

for i in range (fm_start+1, fm_end):
    attribute, content = markdown_to_convert_lines[i].split(":")
    
    match attribute:
        case "title":
            title = content
        case "created":
            date_created = content
        case "modified":
            for j in range(i, fm_end):
                _, date = markdown_to_convert_lines[j].split("- ")
                dates_modified.append(date)

# Handle callouts

