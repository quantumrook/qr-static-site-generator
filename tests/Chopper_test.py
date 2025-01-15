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
