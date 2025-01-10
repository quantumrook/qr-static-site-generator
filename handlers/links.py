import re


markdown_syntax = {
    "display" : r"!{1}\[{1}(?P<alttext>.*)\]{1}\({1}(?P<link>.*)\){1}",
    #"internal" : "\\[{1}(.*)\\]{1}\\({1}(.*)\\){1}",
}

html_syntax = {
    "display" : [
        "<img src=",
        "</img>"
    ],
    # "internal" : [
    #     "<a href=",
    #     "</a>"
    # ]
}

def handle_links(markdown_body: list[str]) -> list[str]:

    for syntax_name, syntax_value in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body


def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str) -> list[str]:
    
    for i, line in enumerate(markdown_body):
        markdown_body[i] = re.sub(syntax_md, '<img src="..\\g<link>" alt="\\g<alttext>" />', line)
    
    return markdown_body