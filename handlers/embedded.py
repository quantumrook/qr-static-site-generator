
import re


def find_embedded_link(chunked_content):
    map_of_embedded_links = { }
    for h2, h2_content in chunked_content.items():
        for h3, h3_content in h2_content.items():
            if h3 == "content":
                list_of_embedded_links = search_block(h3_content)
                if list_of_embedded_links:
                    map_of_embedded_links[h2] = { h3 : list_of_embedded_links}
            else:
                for h4, h4_content in h3_content.items():
                    if h4 == "content":
                        search_block(h4_content)
                    else:
                        for h5, h5_content in h4_content.items():
                            if h5 == "content":
                                search_block(h5_content)
                            else:
                                for h6, h6_content in h5_content.items():
                                    if h6 == "content":
                                        search_block(h6_content)
                                    else:
                                        for sub_h6, sub_h6_content in h6_content.items():
                                            search_block(sub_h6_content)
    if map_of_embedded_links:
        print(map_of_embedded_links)
    return map_of_embedded_links

def search_block(list_of_lists):

    list_of_embedded_links = [ ]
    for list_index, sub_list in enumerate(list_of_lists):
        for sub_list_index, line in enumerate(sub_list):
            regex_match = re.search(r'!\[{2}(?P<file_name>[^\#]*)#(?P<section_name>.*)\]{2}', line)
            if regex_match is None:
                continue
            file_name = regex_match.group(1)
            section_name = regex_match.group(2)
            list_of_embedded_links.append((list_index, sub_list_index, file_name, section_name))
    #print(list_of_embedded_links)
    return list_of_embedded_links

def find_linked_block(files, file_name, section_name):
    pass