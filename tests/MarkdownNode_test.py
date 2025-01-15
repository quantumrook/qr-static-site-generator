import unittest

from markdown_node import MarkdownNode

class TestMarkdownNode(unittest.TestCase):
    
    def test_add_child(self):
        parent_node = MarkdownNode(block_name="Parent", block_data="", parent=None)
        child_node = MarkdownNode(block_name="Child", block_data="Child of Parent", parent=parent_node)
        
        self.assertIs(parent_node.children[-1], child_node)
    
    def test_branch_name_single_child(self):
        parent_node = MarkdownNode(block_name="Parent", block_data="", parent=None)
        child_node = MarkdownNode(block_name="Child", block_data="Child of Parent", parent=parent_node)
        
        self.assertEqual(parent_node.get_branch_name()[0], 'Parent -> Child')
    
    def test_branch_name_multiple_children(self):
        parent_node = MarkdownNode(block_name="Parent", block_data="", parent=None)
        child1_node = MarkdownNode(block_name="Child1", block_data="Child of Parent", parent=parent_node)
        child2_node = MarkdownNode(block_name="Child2", block_data="Child of Parent", parent=parent_node)
        
        branch_names = ['Parent -> Child1', 'Parent -> Child2' ]
        
        matches = [ ]
        for actual_branch_name in parent_node.get_branch_name():
            for theory_branch_name in branch_names:
                if actual_branch_name == theory_branch_name:
                    matches.append(True)
        failed_to_match = False
        if not matches or len(matches) != len(branch_names):
            failed_to_match = True
        for match_result in matches:
            if not match_result:
                failed_to_match = True

        self.assertFalse(failed_to_match)
        
    def test_uneven_branch_name(self):
        parent_node = MarkdownNode(block_name="Parent", block_data="", parent=None)
        child1_node = MarkdownNode(block_name="Child1", block_data="Child of Parent", parent=parent_node)
        child2_node = MarkdownNode(block_name="Child2", block_data="Child of Parent", parent=parent_node)
        
        grandchild_node = MarkdownNode(block_name="Grandchild", block_data="Child of Child2", parent=child2_node)

        branch_names = ['Parent -> Child1', 'Parent -> Child2 -> Grandchild' ]
        
        matches = [ ]
        for actual_branch_name in parent_node.get_branch_name():
            for theory_branch_name in branch_names:
                if actual_branch_name == theory_branch_name:
                    matches.append(True)
        failed_to_match = False
        if not matches or len(matches) != len(branch_names):
            failed_to_match = True
        for match_result in matches:
            if not match_result:
                failed_to_match = True
                
        self.assertFalse(failed_to_match)
    
    def test_get_grandchild_content(self):
        parent_node = MarkdownNode(block_name="Parent", block_data="", parent=None)
        child1_node = MarkdownNode(block_name="Child1", block_data="Child of Parent", parent=parent_node)
        child2_node = MarkdownNode(block_name="Child2", block_data="Child of Parent", parent=parent_node)
        
        grandchild_node = MarkdownNode(block_name="Grandchild", block_data="Child of Child2", parent=child2_node)
        child2_node.children.append(grandchild_node)
        
        self.assertEqual(grandchild_node.block_data, parent_node.get_content_for_branch_name("Grandchild"))
    
    def test_set_grandchild_content(self):
        parent_node = MarkdownNode(block_name="Parent", block_data="", parent=None)
        child1_node = MarkdownNode(block_name="Child1", block_data="Child of Parent", parent=parent_node)
        child2_node = MarkdownNode(block_name="Child2", block_data="Child of Parent", parent=parent_node)
        
        grandchild_node = MarkdownNode(block_name="Grandchild", block_data="Child of Child2", parent=child2_node)
        
        self.assertEqual(grandchild_node.block_data, parent_node.get_content_for_branch_name("Grandchild"))
    
        parent_node.set_content_for_branch_name("Grandchild", "Changed")
        
        self.assertEqual("Changed", parent_node.get_content_for_branch_name("Grandchild"))
        
    def test_get_level(self):
        
        root_node = MarkdownNode("root", "", None)
        self.assertEqual(root_node.get_level(), 0)
        
        level_1 = MarkdownNode("level 1", "", root_node)
        self.assertEqual(level_1.get_level(), 1)
        
        level_2 = MarkdownNode("level 1", "", level_1)
        self.assertEqual(level_2.get_level(), 2)
        
if __name__ == '__main__':
    unittest.main()