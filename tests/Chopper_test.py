import unittest

from private import test_paths
from markdown_node import MarkdownNode

import handlers.chopper


class TestChopper(unittest.TestCase):
    
    def test_no_frontmatter(self):
        lines = [ ]
        with open(test_paths["no frontmatter"], "r") as file:
            lines = file.readlines()
            
        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        
        self.assertFalse(frontmatter)
        self.assertTrue(body)
        
    def test_chunking_body_with_no_frontmatter(self):
        lines = [ ]
        with open(test_paths["no frontmatter"], "r") as file:
            lines = file.readlines()
            
        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        
        self.assertFalse(frontmatter)
        
        chunked_body = handlers.chopper.chop_body_into_nodes(body)
        
        file_as_nodes = MarkdownNode(block_name="article", block_data=["Here's text before the header.\n"], parent=None)
        h2 = MarkdownNode(block_name="## Hello", block_data=['This is a simple markdown file with no frontmatter.\n'], parent=file_as_nodes)
        linebreak = MarkdownNode(block_name="---", block_data=['This was a horizontal rule to test if the function handles it correctly.'], parent=file_as_nodes)
        
        print("Test built:")
        print(file_as_nodes.get_branch_name())
        print("\nFunction built:")
        print(chunked_body.get_branch_name())
        
        found_matches = [ ]
        for test_branch_name in file_as_nodes.get_branch_name():
            for method_branch_name in chunked_body.get_branch_name():
                if test_branch_name == method_branch_name:
                    found_matches.append(True)

        self.assertEqual(len(found_matches), len(file_as_nodes.get_branch_name()))
        
    def test_chunking_body_with_multiple_levels(self):
        lines = [ ]
        with open(test_paths["nested"], "r") as file:
            lines = file.readlines()
            
        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        
        self.assertTrue(frontmatter)
        
        chunked_body = handlers.chopper.chop_body_into_nodes(body)
        
        self.assertIsInstance(chunked_body, MarkdownNode)

        article = MarkdownNode("article", "", None)
        this_is_h2 = MarkdownNode("## This is H2", "", article)
        this_is_h3 = MarkdownNode("### This is H3", "", this_is_h2)
        this_is_h4 = MarkdownNode("#### This is H4", "", this_is_h3)
        this_is_h5 = MarkdownNode("##### This is H5", "", this_is_h4)
        this_is_h6 = MarkdownNode("###### This is H6", "", this_is_h5)
        this_is_another_h6 = MarkdownNode("###### This is Another H6", "", this_is_h5)
        heres_an_h3 = MarkdownNode("### Here's an H3", "", this_is_h2)
        with_its_own_h4 = MarkdownNode("#### With its own H4", "", heres_an_h3)

        found_matches = [ ]
        for test_branch_name in article.get_branch_name():
            for method_branch_name in chunked_body.get_branch_name():
                if test_branch_name == method_branch_name:
                    found_matches.append(True)
        self.assertEqual(len(found_matches), len(article.get_branch_name()))

    def test_chunking_body_with_callouts_and_preformatted(self):
        lines = [ ]
        with open(test_paths["full_suite"], "r") as file:
            lines = file.readlines()
            
        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        chunked_body = handlers.chopper.chop_body_into_nodes(body)
        
        article = MarkdownNode("article", "", None)
        h2_1 = MarkdownNode("## Table of Features Implemented", ['\n', '| Feature | Implemented |\n', '| ------- | ----------- |\n', '| Unordered Lists | Yes |\n', '| Ordered Lists | Yes |\n', '| Task Lists | Yes |\n', '| images, internal | Yes |\n', '| images, external | Yes |\n', '| links, internal | Yes |\n', '| links, external | Yes |\n', '| links, embedded | No |\n', '| Tables | Yes |\n', '| Callouts | Yes |\n', '| Code Blocks | Yes |\n', '| Math | No |\n', '\n', '![small banner](/content/small_banner.png)\n'], article)
        h2_2 = MarkdownNode("## This is H2", ['\n', "Here's **some text**.\n", '\n', 'I should **probably** get *some* ***lorem-ipsum*** in here.\n', '\n', '~~TODO: add lorem-ipsum~~\n', '\n', "Here's an [internal link](#this-is-h2) to the same file. And here's an [internal site](/Example2.md) link. Here's a [link](/Example2.md#other-h2) to a header in the other file.\n", '\n', "Now for the tricky part (?) let's link to the formatting [sheet](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax). And now an external image: ![Engelbart](https://history-computer.com/ModernComputer/Basis/images/Engelbart.jpg)\n"], article)
        h3_1 = MarkdownNode("### Lorem Ipsum", "", h2_2)
        h3_2 = MarkdownNode("### Lists", "", h2_2)
        h4_1 = MarkdownNode("#### But in order:", "", h3_2)
        hr = MarkdownNode("---", "", h3_2)
        h2_3 = MarkdownNode("## Now onto some code", ['\n', 'Here, we create a simple loop in python:\n', '\n', '```python\n', '# before: start, stop, step\n', 'for i in range(start, stop, step):\n', '    f.integrate(i)\n', '```\n', '\n', "Now let's step through this:\n", '\n', '```\n', 'define start\n', 'define stop\n', 'define our step size\n', 'do numerical integration\n', '```\n'], article)

        print("Test built:")
        print(article.get_branch_name())
        print("\nFunction built:")
        print(chunked_body.get_branch_name())
        
        found_matches = [ ]
        for test_branch_name in article.get_branch_name():
            for method_branch_name in chunked_body.get_branch_name():
                if test_branch_name == method_branch_name:
                    found_matches.append(True)
        self.assertEqual(len(found_matches), len(article.get_branch_name()))
        
        # callout_note = MarkdownNode("callout-note", "", h3_1)
        # callout = MarkdownNode("callout", "", h3_1)
        
        # preformatted_python = MarkdownNode("pre-python", "", h2_3)
        # preformatted_text = MarkdownNode("pre-text", "", h2_3)
    
    def test_subchunking(self):
        lines = [ ]
        with open(test_paths["full_suite"], "r") as file:
            lines = file.readlines()
            
        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        chunked_body = handlers.chopper.chop_body_into_nodes(body)
        
        handlers.chopper.chop_nodes_into_subnodes(chunked_body)
        
        self.assertIsInstance(chunked_body, MarkdownNode)