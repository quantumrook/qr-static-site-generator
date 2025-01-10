import re

markdown_syntax = {
    "styles" :
        {
            "bold_italics" : r'\*{3}(?P<content>[^*]*)\*{3}', # ***<content>***
            "bold" : r'\*{2}(?P<content>[^*]*)\*{2}', # **<content>**
            "italics" : r'\*{1}(?P<content>[^*]*)\*{1}', # *<content>*
            "horizontal_rule" : r'^-{3}\n', # ---
            "strikeout" : r'\~{2}(?P<content>.*)\~{2}' # ~~<content>~~
        },
}

replacement_syntax = {
    "styles" :
        {
            "bold_italics" : r'<b><i>\g<content></i></b>', # ***<content>***
            "bold" : r'<b>\g<content></b>', # **<content>**
            "italics" : r'<i>\g<content></i>', # *<content>*
            "horizontal_rule" : "", # ---
            "strikeout" : r'<strike>\g<content></strike>'
        },
}

html_syntax = {
    "styles" : 
        {
            "bold_italics" : 
                [
                    "",
                    ""    
                ],
            "bold" : 
                [
                    "",
                    ""  
                ],
            "italics" : 
                [
                    "",
                    ""
                ],
            "horizontal_rule" : 
                [
                    "<hr />",
                    "\n"
                ],
            "strikeout" : 
                [
                    "",
                    ""
                ]
        },

}

def convert_formatting(markdown_body: list[str])->list[str]:
    
    for format_name, sub_categories in markdown_syntax.items():
        for sub_category_name, md_regex in sub_categories.items():
            html_replacement = replacement_syntax[format_name][sub_category_name]
            html_start, html_end = html_syntax[format_name][sub_category_name]

            new_block = True
            for i, line in enumerate(markdown_body):
                if re.search(md_regex, line) is not None:
                    if new_block:
                        prefix = html_start
                        new_block = False
                    else:
                        prefix = ""
                    markdown_body[i] = prefix + re.sub(md_regex, html_replacement, line)
                    if (i+1) == len(markdown_body) or re.search(md_regex, markdown_body[i+1]) is None:
                        markdown_body[i] += html_end
                        new_block = True

    
    return markdown_body