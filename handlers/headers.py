markdown_syntax = {
    "h6": "###### ",
    "h5": "##### ",
    "h4": "#### ",
    "h3": "### ",
    "h2": "## ",
    "h1": "# "
}

html_syntax = {
    "h6": [
      "<section class=h6><h6 id=",
      "</h6>"  
    ],
    "h5": [
        "<section class=h5><h5 id=",
        "</h5>"
    ],
    "h4": [
        "<section class=h4><h4 id=",
        "</h4>"
    ],
    "h3": [
        "<section class=h3><h3 id=",
        "</h3>"
    ],
    "h2": [
        "<section class=h2><h2 id=",
        "</h2>"
    ],
    "h1": [
        "<section class=h1><h1 id=",
        "</h1>"
    ]
}

def handle_headers(markdown_body: list[str]) -> list[str]:

    for syntax_name, syntax_value in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body


def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str) -> list[str]:
    
    started_section = False
    for line_index, line in enumerate(markdown_body):
        if syntax_md in line:
            if started_section:
                markdown_body[line_index -1 ] += "</section>\n"
                started_section = False
            header_content = line.strip().strip(syntax_md)
            header_alias = header_content.strip().replace(" ", "-")
            markdown_body[line_index] = f'{html_start}{header_alias}">{header_content}{html_end}'
            started_section = True
        if (line_index+1) == len(markdown_body) and started_section:
            markdown_body[line_index] += "</section>\n"
    
    return markdown_body