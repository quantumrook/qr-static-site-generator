from markdown_node import MarkdownNode

def chop(lines: list[str]):
    
    frontmatter, body = separate_frontmatter_from_body(lines)
    
    
    

def separate_frontmatter_from_body(lines: list[str]):
    horizontal_rule_indices = [i for i,x in enumerate(lines) if x == "---\n"]
    if not horizontal_rule_indices or horizontal_rule_indices[0] > 1:
        return [ ], lines
    start_of_frontmatter = horizontal_rule_indices[0]
    end_of_frontmatter = horizontal_rule_indices[1]
    frontmatter = lines[start_of_frontmatter:end_of_frontmatter]
    body = lines[end_of_frontmatter+1:]
    return frontmatter, body

def chop_body_into_nodes(body: list[str]) -> MarkdownNode:
    block_signals = ['# ', '## ', '### ', '#### ', '##### ', '###### ', '---']
    article_node = MarkdownNode("article", None, None)
    
    block_of_content = [ ]
    
    indices = [i for i, x in enumerate(body) for y in block_signals if x.startswith(y)]
    header_levels_present = [y for x in body for y in block_signals if x.startswith(y)]
    header_levels_present = list(dict.fromkeys(header_levels_present))
    
    content_indices = [ ]
    for i, index in enumerate(indices):
        if i+1 == len(indices):
            content_indices.append((index+1, len(body)))
        else:
            content_indices.append((index+1, indices[i+1]-1))
    
    for start, stop in content_indices:
        block_of_content.append(body[start:stop])
    
    name_map = {
        "---" : -1,
        "article" : 0,
    }
    level_counter = 1
    for header_level in header_levels_present:
        if header_level.strip() not in name_map:
            name_map[header_level.strip()] = level_counter
            level_counter += 1


    last_node = article_node
    last_node.parent = article_node
    
    last_node_at_level = { 0 : article_node }
    for i, index in enumerate(indices):
        node_name = body[index].strip()
        node_level = name_map[node_name.split(" ")[0]]
        last_node_level = name_map[last_node.block_name.split(" ")[0]]
        
        if node_level > last_node_level:
            node = MarkdownNode(node_name, block_of_content[i], last_node)
        elif node_level == last_node_level or node_level == -1:
            node = MarkdownNode(node_name, block_of_content[i], last_node.parent)
        else:
            last_node = last_node_at_level[node_level -1]
            node = MarkdownNode(node_name, block_of_content[i], last_node)
        
        last_node = node
        last_node_at_level[node_level] = last_node

    return article_node