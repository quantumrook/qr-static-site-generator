import re


markdown_syntax = {
    "row" : r'\|(?P<content>[^\|\n]*)',
}

html_syntax = {
    "row" : [
        r'<pre>',
        r'</pre>'
    ],
}

def handle_tables(markdown_body: list[str]) -> list[str]:

    for syntax_name, syntax_value in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body


def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str) -> list[str]:

    table_started = False
    headers_complete = False
    for i, line in enumerate(markdown_body):
        row_match = re.findall(syntax_md, line)
        if not row_match and not table_started:
            continue
            
        formatted_line = ""
        row_prefix = ""
        prefix = ""
        suffix = ""
        row_suffix = ""
        
        # if (not row_match and table_started):
        #     table_started = False
        #     row_prefix = "</table>\n"
        
        if row_match and not table_started:
            table_started = True
        
        if not headers_complete:
            formatted_line = "<table>\n"
            row_prefix = '\t<thead>\n\t\t<tr>\n'
            prefix = '\t\t\t<th scope="col">'
            suffix = '</th>\n'
            row_suffix = '\t\t</tr>\n\t</thead>'
        elif headers_complete and table_started:
            formatted_line = ""
            row_prefix = "\t<tr>\n"
            prefix = '\t\t<td>'
            suffix = '</td>\n'
            row_suffix = "\t</tr>"
        
        alignment_line = False
        
        formatted_line += row_prefix
        for match in row_match:
            if not match:
                continue
            if "-" in match:
                alignment_line = True
                headers_complete = True
            formatted_line += prefix + match.strip() + suffix
        formatted_line += row_suffix
        
        if alignment_line:
            formatted_line = ""
        
        markdown_body[i] = formatted_line
        if (i+1) == len(markdown_body):
            markdown_body[-1] += "\n</table>"
    return markdown_body
