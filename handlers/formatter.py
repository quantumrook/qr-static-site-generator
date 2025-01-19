"""Handles the conversion of markdown syntax to html.
"""

import re

from markdown_node import MarkdownNode
from syntax.obsidian import markdown_regex_map, html_regex_map
import syntax.python

styles = ["bold_italics", "bold", "italics", "strikeout"]
links = [
    "image_internal",
    "image_external",
    "same_file",
    "internal_site",
    "internal_site_and_header",
    "external_site"
]
lists = [
    "unordered",
    "ordered",
    "task",
    "task_complete"
]

def handle_formatting(article_node: MarkdownNode):
    """Summary
    """
    for branch in article_node.get_branch_name():
        content_block = article_node.get_content_for_branch_name(branch)
        if content_block is None:
            continue
        for style in styles:
            content_block = handle_syntax(
                content_block, markdown_regex_map[style], html_regex_map[style]
            )
        for link in links:
            content_block = handle_links(
                content_block,
                markdown_regex_map[link],
                html_regex_map[link]
            )
        for list_type in lists:
            content_block = handle_lists(
                content_block,
                markdown_regex_map[list_type],
                html_regex_map[list_type]
            )
        content_block = handle_callouts(content_block)
        content_block = handle_tables(content_block)
        content_block = handle_preformatted(
                content_block,
                markdown_regex_map["multi_line"],
                html_regex_map["multi_line"],
            )
        content_block = handle_misc(content_block, branch)
    return article_node

def handle_syntax(content_block: list[str], md_regex: str, html_tags: list[str], skip_preformatted: bool = True) -> list[str]:
    """Handles the general purpose conversion of markdown to html.
    """
    html_start, html_end, html_block_start, html_block_end = html_tags

    preformatted_block_started = False
    block_started = False
    for i, line in enumerate(content_block):
        if skip_preformatted:
            preformatted_match = re.search(r'^`{3}', line)
            if preformatted_match is not None:
                if preformatted_block_started:
                    preformatted_block_started = False
                    continue
                preformatted_block_started = True

        if preformatted_block_started:
            continue

        regex_match = re.search(md_regex, line)

        if regex_match is None or (i+1) == len(content_block):
            if block_started:
                block_started = False
                content_block[i-1] += html_block_end
            continue

        if not block_started:
            block_started = True
            replacement = html_block_start + html_start + regex_match.group(1) + html_end
            content_block[i] = re.sub(md_regex, replacement, line)
        else:
            replacement = html_start + regex_match.group(1) + html_end
            content_block[i] = re.sub(md_regex, replacement, line)

    return content_block

def handle_tables(content_block: list[str], md_regex: str = r'\|(?P<content>[^\|\n]*)'):
    """Specific logic for handling table conversion
    """

    html_block_start = "<table>"
    html_block_end = "</table>"

    html_element_start = ""
    html_element_end = ""

    html_content_start = "<td>"
    html_content_end = "</td>"

    table_started = False
    preformatted_block_started = False
    offset = 0
    for i, line in enumerate(content_block):
        preformatted_match = re.search(r'^`{3}', line)
        if preformatted_match is not None:
            if preformatted_block_started:
                preformatted_block_started = False
                continue
            preformatted_block_started = True

        if preformatted_block_started:
            continue

        row_match = re.findall(md_regex, line)
        if not row_match and not table_started:
            continue

        formatted_line = ""

        if row_match and not table_started:
            table_started = True
            formatted_line += html_block_start
            html_element_start = "<thead>\n<tr>\n"
            html_content_start = '<th scope="col">'
            html_content_end = '</th>'
            html_element_end = "\n</tr>\n</thead>"
        elif row_match and table_started:
            html_element_start = "<tr>\n"
            html_content_start = "<td>"
            html_content_end = "</td>"
            html_element_end = "\n</tr>"

        alignment_line = False
        formatted_line += html_element_start
        for match in row_match:
            if not match:
                continue
            if "---" in match:
                alignment_line = True
                break
            formatted_line += html_content_start + match.strip() + html_content_end
        formatted_line += html_element_end

        if alignment_line:
            formatted_line = ""
            offset = 1
            continue
        if table_started and line == "\n":
            content_block[i-offset-1] += html_block_end
            content_block[i-offset] = "\n"
            break

        content_block[i-offset] = formatted_line

    return content_block

def handle_callouts(content_block: list[str], md_regex: str = r'^>\s(?P<content>.*)'):
    """Specific logic for handling callout conversion
    """

    html_block_start = '<div id="callout"><blockquote>'
    html_block_end = "</blockquote></div>\n"

    html_element_start = ""
    html_element_end = ""

    html_content_start = "<p>"
    html_content_end = "</p>\n"

    block_started = False
    preformatted_block_started = False

    for i, line in enumerate(content_block):
        preformatted_match = re.search(r'^`{3}', line)
        if preformatted_match is not None:
            if preformatted_block_started:
                preformatted_block_started = False
                continue
            preformatted_block_started = True

        if preformatted_block_started:
            continue

        named_match = re.search(r'^>\s\[\!(?P<callout_type>[\S]*)\]\s', line)
        regex_match = re.search(md_regex, line)

        if not regex_match and not block_started:
            continue

        formatted_line = ""

        if named_match and not block_started:
            block_started = True
            formatted_line += '<div id="callout-' + named_match.group(1) + '"><blockquote>'
        elif regex_match and not block_started:
            block_started = True
            formatted_line += html_block_start

        if regex_match is not None:
            formatted_line += html_element_start + html_content_start
            formatted_line += regex_match.group(1).strip()
            formatted_line += html_content_end + html_element_end

        if block_started and line == "\n":
            content_block[i-1] += html_block_end
            block_started = False
        else:
            content_block[i] = formatted_line

    return content_block

def handle_links(content_block: list[str], md_regex: str, html_tags: list[str]) -> list[str]:
    html_start, *_ = html_tags
    for i, line in enumerate(content_block):
        content_block[i] = re.sub(md_regex, html_start, line)
    return content_block

def handle_preformatted(content_block: list[str], md_regex: str, html_tags: list[str]) -> list[str]:
    html_start, html_end, html_block_start, html_block_end = html_tags

    block_started = False
    for i, line in enumerate(content_block):
        regex_match = re.search(md_regex, line)

        if regex_match is None and not block_started:
            continue

        if not block_started:
            block_started = True
            html_start = f'<code class="{regex_match.group(1)}">'
            content_block[i] = re.sub(md_regex, html_block_start, line)
        elif regex_match is not None:
            content_block[i] = html_block_end + "\n"
            block_started = False
        else:
            line_with_keywords = line.strip("\n")
            for keyword, keyword_regex in syntax.python.reserved_words.items():
                line_with_keywords = re.sub(keyword, keyword_regex, line_with_keywords)
            content_block[i] = html_start + line_with_keywords + html_end + "\n"
    return content_block

def handle_lists(content_block: list[str], md_regex: str, html_tags: list[str]) -> list[str]:
    html_start, html_end, html_block_start, html_block_end = html_tags

    list_element_indices = [ ]
    max_indent_level = 1
    for i, line in enumerate(content_block):
        re_match = re.search(md_regex, line.strip())
        if re_match is not None:
            list_element_indices.append(i)
            max_indent_level = max(max_indent_level, line.count("\t"))

    for indent_level in range(0, max_indent_level + 1):
        block_started = False
        for i, line in enumerate(content_block):
            if line.count("\t") < indent_level:
                if block_started:
                    block_started = False
                    content_block[i-1] += html_block_end + "\n"
                continue
            if line.count("\t") > indent_level:
                continue
            regex_match = re.search(md_regex, line.strip("\t"))
            if regex_match is None and not block_started:
                continue
            elif (regex_match is None and block_started):
                block_started = False
                content_block[i-1] += html_block_end
                continue

            if not block_started:
                block_started = True
                content_block[i] = html_block_start + html_start + regex_match.group(1).strip("\n") + html_end + "\n"
            else:
                content_block[i] = html_start + regex_match.group(1).strip("\n") + html_end + "\n"

            if i + 1 == len(content_block):
                block_started = False
                content_block[i] += html_block_end + "\n"

    return content_block

def handle_misc(content_block: list[str], branch: str) -> list[str]:
    if not branch == "article":
        section_name = branch.split(" -> ")[-1]
        header_level = section_name.count("#")
        section_name = section_name.strip(" #")
        section_name_id = "-".join(section_name.split(" "))
        content_block.insert(0, f'<section class="h{header_level}">\n')
        content_block.insert(0,
            f'<h{header_level} id="{section_name_id}">{section_name}</h{header_level}>\n'
        )

    for i, line in enumerate(content_block):
        if line == "\n":
            content_block[i] = ""
        elif line.startswith("<s>") or line.startswith("<b>") or line.startswith("<i>"):
            content_block[i] = "<p>" + line.strip() + "</p>\n"
        elif not line.startswith("<"):
            content_block[i] = "<p>" + line.strip() + "</p>\n"
    return content_block
