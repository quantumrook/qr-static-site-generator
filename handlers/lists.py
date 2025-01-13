import re

regex_syntax = {
    "unordered" : "^-\\ [^\\[]",
    "ordered" : "^\\d+\\.",
    "task" : "^- \\[\s\\] ",
    "task_complete" : "^- \\[[x]\\] "
}

markdown_syntax = {
    "unordered" : [
        "- "
    ],
    "ordered" : [
        "1. "
    ],
    "task" : [
        "- [ ] "
    ],
    "task_complete" : [ 
        "- [x] "
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
        '<ul>',
        '</ul>'
    ],
    "task_complete" : [
        '<ul>',
        '</ul>'
    ]
}

def handle_lists(markdown_body: list[str]) -> list[str]:
    
    for syntax_name, syntax_values in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        reg_expression = regex_syntax[syntax_name]
        for syntax_value in syntax_values:
            markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end, reg_expression)

    return markdown_body

def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str, reg_expression: str) -> list[str]:

    list_element_indices = [ ]
    for i, line in enumerate(markdown_body):
        re_match = re.search(reg_expression, line.strip())
        if re_match is not None:
            list_element_indices.append(i)

    if not list_element_indices:
        return markdown_body
    
    ordered_list = False
    if syntax_md[0].isdigit():
        syntax_md = syntax_md[1:]
        ordered_list = True
    
    li_prefix = "\t<li>"
    li_suffix = "</li>"
    
    task_list = False
    if "[ ]" in syntax_md:
        task_list = True
        li_prefix = '\t<input type="checkbox" id="listitem" disabled/>\n\t<label for="listitem">'
        li_suffix = "</label>\n\t</br>"
        
    if "[x]" in syntax_md:
        task_list = True
        li_prefix = '\t<input type="checkbox" id="listitem" checked disabled/>\n\t<label for="listitem">'
        li_suffix = "</label>\n\t</br>"
    
    previous_indent = -1
    for i in list_element_indices:
        indent_level = markdown_body[i].split(syntax_md.strip())[0].count("\t")
        list_content = markdown_body[i].strip("\n")

        if ordered_list:
            number_index = list_content.index(syntax_md.strip())
            list_content = list_content[0:number_index-1] + list_content[number_index:]
        
        if indent_level > previous_indent:
            markdown_body[i] = list_content.replace(syntax_md, f"{html_start}\n{li_prefix}") + f"{li_suffix}"
        elif indent_level < previous_indent:
            previous_index = list_element_indices[list_element_indices.index(i)-1]
            previous_content = markdown_body[previous_index].strip("\n")
            markdown_body[previous_index] = previous_content + f"\n\t{html_end}"
            markdown_body[i] = list_content.replace(syntax_md, li_prefix) + f"{li_suffix}"
        else:
            markdown_body[i] = list_content.replace(syntax_md, li_prefix) + f"{li_suffix}"
            
        if (i+1) not in list_element_indices:
            markdown_body[i] += f"\n{html_end}"
        previous_indent = indent_level
    
    return markdown_body
