from handlers.reader import get_templates

def write_files(files, destination_directory: str)-> None:

    filenames = list(files.keys())
    for filename in filenames:
        prepared_template = prepare_template(files[filename])
        dest_filename = filename[:-3] + ".html"
        with open(destination_directory + dest_filename, "w+") as writer:
            writer.writelines(prepared_template)

def prepare_template(file):
    templates = get_templates()
    frontmatter = file["frontmatter"]
    body = file["content"]
    squished_body = body.squish()
    for i, line in enumerate(templates["post.html"]):
        if "{{frontmatter}}" in line:
            last_modified = frontmatter[2][-1].strip("\n")
            last_modified = last_modified.strip('"')
            templates["post.html"][i] = line.replace("{{frontmatter}}", f"Created: {frontmatter[1]} <br/>Last Modified: {last_modified}")
        if "{{post_body}}" in line:
            templates["post.html"][i] = line.replace("{{post_body}}", squished_body)
    squished_post = "".join(templates["post.html"])
    for i, line in enumerate(templates["base.html"]):
        if "{{title}}" in line:
            templates["base.html"][i] = line.replace("{{title}}", frontmatter[0])
        if "{{body}}" in line:
            templates["base.html"][i] = line.replace("{{body}}", squished_post)
    return templates["base.html"]