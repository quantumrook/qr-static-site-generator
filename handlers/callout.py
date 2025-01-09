
def handle_callouts(markdown_body):
    callout_counter = 1
    callout_indices = [i for i, line in enumerate(markdown_body) if "> " in line]
    previous_counter = 0
    for i in callout_indices:
        callout_content = markdown_body[i].strip("\n")
        if previous_counter == callout_counter:
            markdown_body[i] = callout_content.replace("> ", "<br/>\n")
        else:
            markdown_body[i] = callout_content.replace("> ", f'<div id="callout-{callout_counter}"><blockquote>')
            previous_counter = callout_counter
        if (i+1) not in callout_indices:
            markdown_body[i] += "</blockquote></div>\n"
            callout_counter += 1
    
    return markdown_body