class MarkdownNode():
    
    def __init__(self, block_name, block_data, parent):
        self.children = [ ]
        self.block_name = block_name
        self.block_data = block_data
        self.parent = parent
        
        if self.parent is not None:
            self.parent.children.append(self)
        
    
    def get_level(self):
        if self.parent is None:
            return 0
        return self.parent.get_level() + 1
    
    def get_branch_name(self):
        branch_names = [ ]
        if not self.children:
            return [self.block_name]
        for child in self.children:
            for child_name in child.get_branch_name():
                branch_names.append(f"{self.block_name} -> {child_name}")
        return branch_names
    
    def get_content_for_branch_name(self, branch_name):
        if branch_name == self.block_name:
            return self.block_data
        
        this_branch_names = self.get_branch_name()
        not_found = True
        for this_branch in this_branch_names:
            if branch_name in this_branch:
                not_found = False
        
        if not_found:
            return ""
        
        for child in self.children:
            child_answer = child.get_content_for_branch_name(branch_name)
            if child_answer:
                return child_answer
            
    def set_content_for_branch_name(self, branch_name, branch_data):
        if branch_name == self.block_name:
            self.block_data = branch_data
        
        this_branch_names = self.get_branch_name()
        not_found = True
        for this_branch in this_branch_names:
            if branch_name in this_branch:
                not_found = False
        
        if not_found:
            return ""
        
        for child in self.children:
            child.set_content_for_branch_name(branch_name, branch_data)
            
if __name__ == "__main__":
    h2 = MarkdownNode("Lorem Ipsum would be over kill", "h2")
    h3 = MarkdownNode("Here are two reasons why", "h3")
    h2.children.append(h3)

    h4a = MarkdownNode("Reason 1", "h4a")
    h4b = MarkdownNode("Reason 2", "h4b")
    h3.children.append(h4a)
    h3.children.append(h4b)

    print(h2.get_branch_name()) # ['h2 -> h3 -> h4a', 'h2 -> h3 -> h4b']

    print(h2.get_content_for_branch_name("h4b"))
    print(h4a.block_data)
    h2.set_content_for_branch_name("h4a", "I've been replaced!")
    print(h4a.block_data)
