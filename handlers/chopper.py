from markdown_node import MarkdownNode

def chop(lines: list[str]):

    frontmatter, body = separate_frontmatter_from_body(lines)
    frontmatter = __handle_frontmatter(frontmatter)
    article_node = chop_body_into_nodes(body)

    return frontmatter, article_node

def separate_frontmatter_from_body(lines: list[str]):
    horizontal_rule_indices = [i for i,x in enumerate(lines) if x == "---\n"]
    if not horizontal_rule_indices or horizontal_rule_indices[0] > 1:
        return [ ], lines
    start_of_frontmatter = horizontal_rule_indices[0]
    end_of_frontmatter = horizontal_rule_indices[1]
    frontmatter = lines[start_of_frontmatter:end_of_frontmatter]
    body = lines[end_of_frontmatter+1:]
    return frontmatter, body

def __handle_frontmatter(lines: list[str]) -> tuple[str, str, list[str]]:
    title = ""
    date_created = ""
    dates_modified = [ ]
    for i, line in enumerate(lines):
        attribute, _, content = line.partition(":")
        content = content.strip() #get rid of whitespace and newline characters
        match attribute:
            case "title":
                title = content.strip('"')
            case "created":
                date_created = content.strip('"')
            case "modified":
                for j in range(i+1, len(lines)):
                    _, date = lines[j].split("- ")
                    dates_modified.append(date.strip('"'))
    return (title, date_created, dates_modified)

def __get_section_indices(body: list[str]) -> list[int]:
    section_signals = ['# ', '## ', '### ', '#### ', '##### ', '###### ', '---']
    indices = [i for i, x in enumerate(body) for y in section_signals if x.startswith(y)]
    block_signals = ['```']
    indices_to_ignore = [i for i, x in enumerate(body) for y in block_signals if x.startswith(y)]
    cleaned_indices = [ ]
    for index in indices:
        found_issue = False
        for i in range(0, len(indices_to_ignore), 2):
            start = indices_to_ignore[i]
            stop = indices_to_ignore[i+1]
            
            if index > start and index < stop:
                found_issue = True
        if not found_issue:
            cleaned_indices.append(index)
    return cleaned_indices
    
def __get_section_content(indices: list[int], body: list[str]) -> list[list[str]]:
    blocks_of_content = [ ]
    for i, index in enumerate(indices):
        if i+1 == len(indices):
            blocks_of_content.append(body[index+1:len(body)])
        else:
            blocks_of_content.append(body[index+1:indices[i+1]-1])
    return blocks_of_content

def __get_section_name_to_level_map(body: list[str], section_indices: list[int]) -> dict[str, int]:
    block_signals = ['# ', '## ', '### ', '#### ', '##### ', '###### ', '---']
    
    section_headers = [ ]
    for index in section_indices:
        section_headers.append(body[index])
    
    header_levels_present = [y for x in section_headers for y in block_signals if x.startswith(y)]
    header_levels_present = list(dict.fromkeys(header_levels_present))
    
    name_map = {
        "---" : -1,
        "article" : 0,
    }
    level_counter = 1
    for header_level in header_levels_present:
        if header_level.strip() not in name_map:
            name_map[header_level.strip()] = level_counter
            level_counter += 1
    return name_map

def chop_body_into_nodes(body: list[str]) -> MarkdownNode:
    section_header_indices = __get_section_indices(body)
    section_content = __get_section_content(section_header_indices, body)
    
    section_name_map = __get_section_name_to_level_map(body, section_header_indices)
    
    if not section_header_indices:
        return MarkdownNode("article", body, None)
    
    article_node = MarkdownNode("article", body[:section_header_indices[0]], None)
    last_node = article_node
    
    last_node_at_level = { 0 : article_node }
    for i, index in enumerate(section_header_indices):
        node_name = body[index].strip()
        node_level = section_name_map[node_name.split(" ")[0]]
        last_node_level = section_name_map[last_node.block_name.split(" ")[0]]
        
        if last_node_level == -1:
            last_node = last_node_at_level[node_level -1]
            node = MarkdownNode(node_name, section_content[i], last_node)
        elif node_level > last_node_level:
            node = MarkdownNode(node_name, section_content[i], last_node)
        elif node_level == last_node_level or node_level == -1:
            node = MarkdownNode(node_name, section_content[i], last_node.parent)
        else:
            last_node = last_node_at_level[node_level -1]
            node = MarkdownNode(node_name, section_content[i], last_node)
        
        last_node = node
        last_node_at_level[node_level] = last_node

    return article_node
