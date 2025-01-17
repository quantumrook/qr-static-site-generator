

import re


def handle_syntax(content_block: list[str], md_regex: str, html_tags: list[str], skip_preformatted: bool = True) -> list[str]:
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
                else:
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

