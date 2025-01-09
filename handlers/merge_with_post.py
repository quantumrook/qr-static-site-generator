from private import base_path, templates

def merge_with_post(markdown_body, frontmatter) -> str:

    squished_body = __squish_body(markdown_body)
    post_html_template = __get_template()
    
    squished_post = __squish_post(frontmatter, post_html_template, squished_body)
    return squished_post
        
def __squish_body(markdown_body: list[str])-> str:
    squished_body = ""
    have_reached_text = False

    for line in markdown_body:
        if line is "\n" and have_reached_text == False:
            continue
        else:
            have_reached_text = True
        if line is "\n":
            squished_body += "<br />"
        squished_body += line
    return squished_body

def __get_template() -> list[str]:
    post_fp = f"{base_path}{templates["post"]}"
    post_html_template = [ ]
        
    with open(post_fp, "r") as file:
        post_html_template = file.readlines()
    
    return post_html_template

def __squish_post(frontmatter, post_html_template, squished_body)-> str:
    squished_post = ""
    for line in post_html_template:
        if "{{frontmatter}}" in line:
            last_modified = frontmatter[2].strip("\n")
            last_modified = last_modified.strip('"')
            line = line.replace("{{frontmatter}}", f"Created: {frontmatter[1]} <br/>Last Modified: {last_modified}")
        if "{{post_body}}" in line:
            line = line.replace("{{post_body}}", squished_body)

        squished_post += line
    return squished_post