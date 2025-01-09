markdown_syntax = {
    "unordered" : [
        "- "
    ],
    "ordered" : [
        "1. "
    ],
    "task" : [
        "[ ] ",
        "[x] "
    ]
}

html_syntax = {
    "unordered" : [
        "<ul>",
        "</ul>"
    ],
    "ordered" : [
        "<ol>",
        "</ol>"
    ],
    "task" : [
        "<ul>",
        "</ul>"
    ]
}

def handle_lists(markdown_body: list[str]) -> list[str]:
    
    for syntax_name, syntax_values in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        for syntax_value in syntax_values:
            if syntax_value == "1.":
                continue
            markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body

def __handle_syntax(markdown_body: list[str], syntax_md, html_start, html_end) -> list[str]:
    list_counter = 1
    list_element_indices = [i for i, line in enumerate(markdown_body) if syntax_md in line]
    previous_counter = 0
    
    if not list_element_indices:
        return markdown_body
    
    previous_indent = markdown_body[list_element_indices[0]].count(" ")
    for i in list_element_indices:
        indent_level = markdown_body[i].count(" ")
        list_content = markdown_body[i].strip("\n")
        if previous_counter == list_counter:
            if indent_level > previous_indent:
                markdown_body[i] = list_content.replace(syntax_md, f"{html_start}<li>") + "</li>\n"
            elif indent_level < previous_indent:
                markdown_body[i] = list_content.replace(syntax_md, "<li>") + f"</li>{html_end}\n"
            else:
                markdown_body[i] = list_content.replace(syntax_md, "<li>") + "</li>\n"
        else:
            markdown_body[i] = list_content.replace(syntax_md, f'{html_start}<li>') + "</li>\n"
            previous_counter = list_counter
        if (i+1) not in list_element_indices:
            markdown_body[i] += f"{html_end}\n"
            list_counter += 1
        previous_indent = indent_level
    
    return markdown_body
    