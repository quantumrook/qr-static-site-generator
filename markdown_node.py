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
        branch_names.append(self.block_name)
        for child in self.children:
            for child_name in child.get_branch_name():
                branch_names.append(f"{self.block_name} -> {child_name}")
        return branch_names

    def get_content_for_branch_name(self, branch_name):
        if branch_name.split(" -> ")[-1] == self.block_name:
            return self.block_data

        this_branch_names = self.get_branch_name()
        not_found = True
        for this_branch in this_branch_names:
            if branch_name in this_branch:
                not_found = False

        if not_found:
            return ""

        _, *rest_of_branch = branch_name.split(" -> ")
        if not rest_of_branch:
            return ""

        trimmed_branch = ""
        for i, branch in enumerate(rest_of_branch):
            if branch:
                trimmed_branch += branch
            if i + 1 < len(rest_of_branch):
                trimmed_branch += " -> "

        for child in self.children:
            child_answer = child.get_content_for_branch_name(trimmed_branch)
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

    def squish(self) -> str:
        squished = ""
        section_end = ""
        for child in self.children:
            squished += child.squish()
        self_squish = "".join(self.block_data)
        if not self.block_name == "article" and not self.block_name == "---":
            section_end = "</section>\n"
        if self.block_name == "---":
            section_end = "<hr />"
        return self_squish + squished + section_end
