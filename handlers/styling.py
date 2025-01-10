markdown_syntax = {
    "bold_italics" : [
        "***",
        "___"
    ],
    "bold" : [
        "**",
        "__"
    ],
    "italics" : [
        "*",
        "_"
    ],
    "strikethrough" : [
        "~~"
    ]
}

html_syntax = {
    "bold_italics" : [
        "<b><i>",
        "</i></b>"
    ],
    "bold" : [
        "<b>",
        "</b>"
    ],
    "italics" : [
        "<i>",
        "</i>"
    ],
    "strikethrough" : [
        "<strike>",
        "</strike>"
    ]
}

def handle_styling(markdown_body) -> list[str]:

    for syntax_name, syntax_values in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        for syntax_value in syntax_values:
            markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    markdown_body = __handle_horizontal_rule(markdown_body)

    return markdown_body

def __handle_syntax(markdown_body, syntax_md, html_start, html_end) -> list[str]:

    syntax_length = len(syntax_md)

    for line_index, line in enumerate(markdown_body):
        start_of_block = True
        if syntax_md in line:
            words = line.split(" ")
            for i, word in enumerate(words):
                if syntax_md in word:
                    prefix = word.strip()[:syntax_length]
                    suffix = word.strip()[-syntax_length:]
                    if prefix == syntax_md and suffix == syntax_md:
                        words[i] = html_start + word[syntax_length:].replace(syntax_md, html_end)
                    elif start_of_block:
                        words[i] = word.replace(syntax_md, html_start)
                        start_of_block = False
                    else:
                        words[i] = word.replace(syntax_md, html_end)
                        start_of_block = True
            markdown_body[line_index] = " ".join(words)

    return markdown_body

def __handle_horizontal_rule(markdown_body: list[str]) -> list[str]:
    syntax_md = "---"
    
    for line_index, line in enumerate(markdown_body):
        if syntax_md == line.strip():
            markdown_body[line_index] = "<hr />\n"
            
    return markdown_body