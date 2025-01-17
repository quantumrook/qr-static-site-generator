
class BaseThing():
    
    def __init__(self, markdown: str, regex: str, html_start: str, html_end: str):
        self.markdown = markdown
        self.regex = regex
        self.html_start = html_start
        self.html_end = html_end

class BlockThing(BaseThing):
    
    def __init__(self, markdown, regex, html_start, html_end, html_block_start, html_block_end):
        super().__init__(markdown, regex, html_start, html_end)
        self.block_start = html_block_start
        self.block_end = html_block_end

bold = BaseThing(
    markdown= "**",
    regex= r'\*{2}(?P<content[^*]*)\*{2}',
    html_start= "<b>",
    html_end= "</b>"
)

unnamed_callout = BlockThing(
    markdown= ">",
    regex=r'^>\s(?P<content>.*)',
    html_start= "<p>",
    html_end="</p>",
    html_block_start= '<div id="callout"><blockquote>',
    html_block_end= '</blockquote></div>'
)

## ------------------------------------------

markdown_regex_html_map = {
    
    "bold" : {
        "regex_find" : r'\*{2}(?P<content>[^*]*)\*{2}',
        "regex_replace" : r'<b>\g<content></b>'
    },
    
    "unnamed_callout" : {
        "regex_find" : r'^>\s(?P<content>.*)',
        "regex_replace" : r'<div id="callout">\n<blockquote>\n\g<content>\n</blockquote>\n</div>\n'
    }
}

## ------------------------------------------

markdown_regex_map = {
    "bold_italics" : r'\*{3}(?P<content>.*)\*{3}',
    "bold" : r'\*{2}(?P<content>.*)\*{2}',
    "italics" : r'\*{1}(?P<content>[^*]*)\*{1}',
    "strikeout" : r'\~{2}(?P<content>.*)\~{2}',
    
    # "horizontal_rule" : r'^-{3}\n',
    # "h6" : r'^\#{6}\s(?P<content>.*)\n',
    # "h5" : r'^\#{5}\s(?P<content>.*)\n',
    # "h4" : r'^\#{4}\s(?P<content>.*)\n',
    # "h3" : r'^\#{3}\s(?P<content>.*)\n',
    # "h2" : r'^\#{2}\s(?P<content>.*)\n',
    # "h1" : r'^\#{1}\s(?P<content>.*)\n',
    # "unnamed_callout" : r'^>\s(?P<content>.*)',
}

html_regex_map = {
    "bold_italics" : [
        r'<b><i>',
        r'</i></b>',
        r'',
        r''  
    ],
    "bold" : [
        r'<b>',
        r'</b>',
        r'',
        r''
    ],
    "italics" : [
        r'<i>',
        r'</i>',
        r'',
        r''
    ],
    "strikeout" : [
        r'<s>',
        r'</s>',
        r'',
        r''
    ],
    
    # "horizontal_rule" : [
    #     r'<hr />',
    #     r'',
    #     r'',
    #     r''
    # ],
    
    # "h6" : [
    #     r'<h6 id="\g<content>">',
    #     r'</h6>',
    #     r'<section class="h6">',
    #     r'</section>'
    # ],
    # "h5" : [
    #     r'<h5 id="\g<content>">',
    #     r'</h5>',
    #     r'<section class="h5">',
    #     r'</section>'
    # ],
    # "h4" : [
    #     r'<h4 id="\g<content>">',
    #     r'</h4>',
    #     r'<section class="h4">',
    #     r'</section>'
    # ],
    # "h3" : [
    #     r'<h3 id="\g<content>">',
    #     r'</h3>',
    #     r'<section class="h3">',
    #     r'</section>'
    # ],
    # "h2" : [
    #     r'<h2 id="\g<content>">',
    #     r'</h2>',
    #     r'<section class="h2">',
    #     r'</section>'
    # ],
    # "h1" : [
    #     r'<h1 id="\g<content>">',
    #     r'</h1>',
    #     r'<section class="h1">',
    #     r'</section>'
    # ],
    # "unnamed_callout" : [
    #     r'<p>',
    #     r'</p>',
    #     r'<div id="callout">\n<blockquote>\n',
    #     r'</blockquote>\n</div>\n'
    # ]
}