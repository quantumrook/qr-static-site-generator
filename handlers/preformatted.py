import re


markdown_syntax = {
    "multi_line" : r'`{3}(?P<language>\S*)',
}

html_syntax = {
    "multi_line" : [
        r'<pre><code class="\g<language>">',
        r'</code></pre>'
    ],
}

def handle_preformatted_blocks(markdown_body: list[str]) -> list[str]:

    for syntax_name, syntax_value in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body


def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str) -> list[str]:
    
    block_started = False
    for i, line in enumerate(markdown_body):
        
        regex_match = re.search(syntax_md, line)
        if regex_match is not None:
            if not block_started:
                markdown_body[i] = re.sub(syntax_md, html_start, line)
                block_started = True
            else:
                markdown_body[i] = re.sub(syntax_md, html_end, line)
                block_started = False
    
    return markdown_body