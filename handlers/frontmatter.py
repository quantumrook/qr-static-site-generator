

def handle_frontmatter(markdown_to_convert_lines):
    fm_start = markdown_to_convert_lines.index("---\n")
    fm_end = markdown_to_convert_lines[1:].index("---\n")

    markdown_frontmatter = markdown_to_convert_lines[fm_start:fm_end]
    markdown_body = markdown_to_convert_lines[(fm_end+2):]

    title = ""
    date_created = ""
    dates_modified = [ ]

    for i in range (fm_start+1, fm_end):
        attribute, _, content = markdown_to_convert_lines[i].partition(":")
        content = content.strip() #get rid of whitespace and newline characters
        match attribute:
            case "title":
                title = content.strip('"')
            case "created":
                date_created = content.strip('"')
            case "modified":
                for j in range(i+1, fm_end+1):
                    _, date = markdown_to_convert_lines[j].split("- ")
                    dates_modified.append(date.strip('"'))
    
    return (title, date_created, dates_modified, markdown_body)