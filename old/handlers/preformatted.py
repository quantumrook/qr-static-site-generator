import re


markdown_syntax = {
    "multi_line" : r'`{3}(?P<language>\S*)',
}

html_syntax = {
    "multi_line" : [
        r'<pre>',
        r'</pre>'
    ],
}

reserved_words = {
    "text" : { },
    "python" : {
        r'#+(?P<comment>[ ]*[\S ]*)' : r'<span class="comment">#\g<comment></span>\n',
        r'(?P<leadingspace>\s*)(?P<name>\S*)\(' : r'\g<leadingspace><span class="method">\g<name></span>(',
        r'^(?P<leadingspace>\s*)[f][o][r]' : r'\g<leadingspace><span class="keyword">for</span>',
        r'(?P<leadingspace>\s)[i][n]' : r'\g<leadingspace><span class="keyword">in</span>'
    },
}

def handle_preformatted_blocks(markdown_body: list[str]) -> list[str]:

    for syntax_name, syntax_value in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body


def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str) -> list[str]:
    
    block_started = False
    language = "text"
    for i, line in enumerate(markdown_body):
            regex_match = re.search(syntax_md, line)
            if regex_match is not None:
                if not block_started:
                    if regex_match.group(1):
                        language = regex_match.group(1)
                    markdown_body[i] = re.sub(syntax_md, html_start, line)
                    block_started = True
                else:
                    markdown_body[i] = re.sub(syntax_md, html_end, line)
                    block_started = False
                    language = "text"
            else:
                if block_started:
                    line_with_keywords = line 
                    for keyword, kw_regex in reserved_words[language].items():
                        line_with_keywords = re.sub(keyword, kw_regex, line_with_keywords)
                    markdown_body[i] =f'<code class="{language}">' + line_with_keywords.strip("\n") + "</code>"
    
    return markdown_body
