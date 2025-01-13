import re


markdown_syntax = {
    "named_callout" : r'^>\s\[\!(?P<callout_type>[\S]*)\]\s',
    "unnamed_callout" : r'^>\s(?P<content>.*)'
}

html_syntax = {
    "named_callout" : [
            r'<div id="callout\g<callout_type>">',
            r'</div>'
        ],
    "unnamed_callout" : [
            r'<blockquote>\g<content></blockquote>',
            r''
        ],
}

def handle_preformatted_blocks(markdown_body: list[str]) -> list[str]:

    for syntax_name, syntax_value in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body


def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str) -> list[str]:

    block_started = False
    callout_type = ""
    for i, line in enumerate(markdown_body):
        callout_match = re.search(r'^> ', line)
        callout_name = re.search(r'^>\s\[\!(?P<callout_type>[\S]*)\]\s', line)
        callout_content = re.search(r'^>\s(?P<content>.*)', line)
        if callout_match is None:
            if block_started:
                markdown_body[i] = "</blockquote></div>\n"
                block_started = False
            continue
        
        if not block_started:
            block_started = True
            if callout_name is not None:
                markdown_body[i] = re.sub(r'^>\s\[\!(?P<callout_type>[\S]*)\]\s', r'<div id="callout-\g<callout_type>"><blockquote>', line)
            else:
                markdown_body[i] = re.sub(r'^> ', '<div id="callout"><blockquote>\n\t', line) + "<br />"
        elif callout_content is not None:
            markdown_body[i] = "\t" + callout_content.group(1) + "<br />"

        if (i+1) == len(markdown_body):
            markdown_body[i] += "\n</blockquote></div>"
    return markdown_body


def handle_callouts(markdown_body):
    
    return handle_preformatted_blocks(markdown_body)