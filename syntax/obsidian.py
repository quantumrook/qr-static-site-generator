
markdown_regex_map = {
    "bold_italics" : r'\*{3}(?P<content>.*)\*{3}',
    "bold" : r'\*{2}(?P<content>.*)\*{2}',
    "italics" : r'\*{1}(?P<content>[^*]*)\*{1}',
    "strikeout" : r'\~{2}(?P<content>.*)\~{2}',
    "image_internal" : r"!{1}\[{1}(?P<alttext>.*)\]{1}\({1}(?![http])(?P<link>.*)\){1}",
    "image_external" : r"!{1}\[{1}(?P<alttext>.*)\]{1}\({1}(?P<link>.*)\){1}",
    "same_file" : r'[^!]\[(?P<displaytext>.*)\]\((?P<headerlink>#{1}[^)]*)\)',
    "internal_site" : r'[^!]\[(?P<displaytext>[^]]*)\]\((?![http])(?P<internallink>[^#).]*)(\.+\S{2})(?P<headerlink>[^#)]*)\)',
    "internal_site_and_header" : r'[^!]\[(?P<displaytext>[^]]*)\]\((?![http])(?P<internallink>[^#).]*)(\.+\S{2})(?P<headerlink>[^)]*)\)',
    "external_site" : r'[^!]\[(?P<displaytext>[^]]*)\]\((?P<externallink>[^#)]*)\)',
    "multi_line" : r'`{3}(?P<language>\S*)',
    "unordered" : r'^-\ (?=[^\[])(?P<content>.*)',
    "ordered" : r'^\d+\.(?P<content>.*)',
    "task" : r'^-\ \[{1}\ \]{1}(?P<content>.*)',
    "task_complete" : r'^-\ \[{1}[x]{1}\]{1}(?P<content>.*)'
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
    "image_internal" : [
        r' <img src="..\g<link>" alt="\g<alttext>" />',
        r'',
        r'',
        r''
    ],
    "image_external" : [
        r' <img src="\g<link>" alt="\g<alttext>" />',
        r'',
        r'',
        r''
    ],
    "same_file" : [
        r' <a href="\g<headerlink>">\g<displaytext></a>',
        r'',
        r'',
        r''
    ],
    "internal_site" : [
        r' <a href="..\g<internallink>.html">\g<displaytext></a>',
        r'',
        r'',
        r''
    ],
    "internal_site_and_header" : [
        r' <a href="..\g<internallink>.html\g<headerlink>">\g<displaytext></a>',
        r'',
        r'',
        r''
    ],
    "external_site" : [
        r' <a href="\g<externallink>">\g<displaytext></a>',
        r'',
        r'',
        r''
    ],
    "multi_line" : [
        r'<code>',
        r'</code>',
        r'<pre>',
        r'</pre>'
    ],
    "unordered" : [
        "<li>",
        "</li>",
        "<ul>",
        "</ul>"
    ],
    "ordered" : [
        "<li>",
        "</li>",
        "<ol>",
        "</ol>"
    ],
    "task" : [
        '<li><input type="checkbox" id="listitem" disabled/><label for="listitem">',
        "</label></li>",
        '<ul>',
        '</ul>'
    ],
    "task_complete" : [
        '<li><input type="checkbox" id="listitem" checked disabled/><label for="listitem">',
        "</label></li>",
        '<ul>',
        '</ul>'
    ]
}
