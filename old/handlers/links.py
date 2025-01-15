import re


markdown_syntax = {
    "image_internal" : r"!{1}\[{1}(?P<alttext>.*)\]{1}\({1}(?![http])(?P<link>.*)\){1}",
    "image_external" : r"!{1}\[{1}(?P<alttext>.*)\]{1}\({1}(?P<link>.*)\){1}",
    "same_file" : r'[^!]\[(?P<displaytext>.*)\]\((?P<headerlink>#{1}[^)]*)\)',
    "internal_site" : r'[^!]\[(?P<displaytext>[^]]*)\]\((?![http])(?P<internallink>[^#).]*)(\.+\S{2})(?P<headerlink>[^#)]*)\)',
    "internal_site_and_header" : r'[^!]\[(?P<displaytext>[^]]*)\]\((?![http])(?P<internallink>[^#).]*)(\.+\S{2})(?P<headerlink>[^)]*)\)',
    "external_site" : r'[^!]\[(?P<displaytext>[^]]*)\]\((?P<externallink>[^#)]*)\)'
}

html_syntax = {
    "image_internal" : [
        r' <img src="..\g<link>" alt="\g<alttext>" />',
        ""
    ],
    "image_external" : [
        r' <img src="\g<link>" alt="\g<alttext>" />',
        ""
    ],
    "same_file" : [
        r' <a href="\g<headerlink>">\g<displaytext></a>',
        ""
    ],
    "internal_site" : [
        r' <a href="..\g<internallink>.html">\g<displaytext></a>',
        ""
    ],
    "internal_site_and_header" : [
        r' <a href="..\g<internallink>.html\g<headerlink>">\g<displaytext></a>',
        ""
    ],
    "external_site" : [
        r' <a href="\g<externallink>">\g<displaytext></a>',
        ""
    ]
}

def handle_links(markdown_body: list[str]) -> list[str]:

    for syntax_name, syntax_value in markdown_syntax.items():
        html_start, html_end = html_syntax[syntax_name]
        markdown_body = __handle_syntax(markdown_body, syntax_value, html_start, html_end)

    return markdown_body


def __handle_syntax(markdown_body: list[str], syntax_md: str, html_start: str, html_end: str) -> list[str]:
    
    for i, line in enumerate(markdown_body):
        markdown_body[i] = re.sub(syntax_md, html_start, line)
    
    return markdown_body