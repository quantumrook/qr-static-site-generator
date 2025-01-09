def handle_headers(markdown_body) -> list[str]:
    for j in range(6,0,-1):
        header_level = ""
        for k in range(j):
            header_level += "#"
        header_level += " "
        
        header_indicies = [i for i, line in enumerate(markdown_body) if header_level in line]
        for i in header_indicies:
            header_line = markdown_body[i].strip()
            markdown_body[i] = header_line.replace(header_level, f"<h{j}>") + f"</h{j}>\n"
    return markdown_body