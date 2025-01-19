import unittest

import handlers.formatter
from private import test_paths
from markdown_node import MarkdownNode

from handlers.formatter import handle_syntax
import handlers.chopper

from syntax.obsidian import markdown_regex_map, html_regex_map

class TestBold(unittest.TestCase):
    
    def test_no_bold(self):
        desired_output = ["Hello.\n", "There's no string with the bold syntax in this list.\n", "Goodbye.\n"]
        content_without_bold = ["Hello.\n", "There's no string with the bold syntax in this list.\n", "Goodbye.\n"]
        
        formatted_content = handle_syntax(content_without_bold, markdown_regex_map["bold"], html_regex_map["bold"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])
    
    def test_bold(self):
        desired_output = ["Hello.\n", "There's one string with the <b>bold</b> syntax in this list.\n", "Goodbye.\n"]
        content_to_format = ["Hello.\n", "There's one string with the **bold** syntax in this list.\n", "Goodbye.\n"]
        formatted_content = handle_syntax(content_to_format, markdown_regex_map["bold"], html_regex_map["bold"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])

    def test_bold_with_italics_present(self):
        desired_output = ["Hello.\n", "There's one string with the <b>bold *syntax*</b> in this list.\n", "Goodbye.\n"]
        content_to_format = ["Hello.\n", "There's one string with the **bold *syntax*** in this list.\n", "Goodbye.\n"]
        formatted_content = handle_syntax(content_to_format, markdown_regex_map["bold"], html_regex_map["bold"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])

class TestItalics(unittest.TestCase):
    
    def test_no_italics(self):
        desired_output = ["Hello.\n", "There's no string with the italics syntax in this list.\n", "Goodbye.\n"]
        content_without_italics = ["Hello.\n", "There's no string with the italics syntax in this list.\n", "Goodbye.\n"]
        
        formatted_content = handle_syntax(content_without_italics, markdown_regex_map["italics"], html_regex_map["italics"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])
            
    def test_italics(self):
        desired_output = ["Hello.\n", "There's one string with the <i>italics</i> syntax in this list.\n", "Goodbye.\n"]
        content_to_format = ["Hello.\n", "There's one string with the *italics* syntax in this list.\n", "Goodbye.\n"]
        
        formatted_content = handle_syntax(content_to_format, markdown_regex_map["italics"], html_regex_map["italics"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])
            
    def test_bold_with_italics_present(self):
        desired_output = ["Hello.\n", "There's one string with the <b>bold <i>syntax</i></b> in this list.\n", "Goodbye.\n"]
        content_to_format = ["Hello.\n", "There's one string with the **bold *syntax*** in this list.\n", "Goodbye.\n"]
        formatted_content = handle_syntax(content_to_format, markdown_regex_map["bold"], html_regex_map["bold"])
        formatted_content = handle_syntax(formatted_content, markdown_regex_map["italics"], html_regex_map["italics"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])

class TestStrikeout(unittest.TestCase):
    
    def test_no_strike(self):
        desired_output = ["Hello.\n", "There's no string with the strike syntax in this list.\n", "Goodbye.\n"]
        content_without = ["Hello.\n", "There's no string with the strike syntax in this list.\n", "Goodbye.\n"]
        
        formatted_content = handle_syntax(content_without, markdown_regex_map["strikeout"], html_regex_map["strikeout"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])
            
    def test_strike(self):
        desired_output = ["Hello.\n", "There's one string with the <s>strike</s> syntax in this list.\n", "Goodbye.\n"]
        content_to_format = ["Hello.\n", "There's one string with the ~~strike~~ syntax in this list.\n", "Goodbye.\n"]
        
        formatted_content = handle_syntax(content_to_format, markdown_regex_map["strikeout"], html_regex_map["strikeout"])
        
        for i in range(len(formatted_content)):
            self.assertEqual(desired_output[i], formatted_content[i])

class TestWithNodes(unittest.TestCase):
    
    def test_styling(self):
        lines = [ ]
        with open(test_paths["full_suite"], "r") as file:
            lines = file.readlines()
            
        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        chunked_body = handlers.chopper.chop_body_into_nodes(body)
        
        article = MarkdownNode("article", ['\n', '```\n', '**bold**\n', '*italics*\n', '***bold-italics***\n', '~~strike~~\n', '```\n', '\n'], None)
        h2_1 = MarkdownNode("## Table of Features Implemented", ['\n', '| Feature | Implemented |\n', '| ------- | ----------- |\n', '| Unordered Lists | Yes |\n', '| Ordered Lists | Yes |\n', '| Task Lists | Yes |\n', '| images, internal | Yes |\n', '| images, external | Yes |\n', '| links, internal | Yes |\n', '| links, external | Yes |\n', '| links, embedded | No |\n', '| Tables | Yes |\n', '| Callouts | Yes |\n', '| Code Blocks | Yes |\n', '| Math | No |\n', '\n', '![small banner](/content/small_banner.png)\n'], article)
        h2_2 = MarkdownNode("## This is H2", ['\n', "Here's **some text**.\n", '\n', 'I should **probably** get *some* ***lorem-ipsum*** in here.\n', '\n', '~~TODO: add lorem-ipsum~~\n', '\n', "Here's an [internal link](#this-is-h2) to the same file. And here's an [internal site](/Example2.md) link. Here's a [link](/Example2.md#other-h2) to a header in the other file.\n", '\n', "Now for the tricky part (?) let's link to the formatting [sheet](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax). And now an external image: ![Engelbart](https://history-computer.com/ModernComputer/Basis/images/Engelbart.jpg)\n"], article)
        h3_1 = MarkdownNode("### Lorem Ipsum", "", h2_2)
        h3_2 = MarkdownNode("### Lists", "", h2_2)
        h4_1 = MarkdownNode("#### But in order:", "", h3_2)
        hr = MarkdownNode("---", "", h3_2)
        h2_3 = MarkdownNode("## Now onto some code", ['\n', 'Here, we create a simple loop in python:\n', '\n', '```python\n', '# before: start, stop, step\n', 'for i in range(start, stop, step):\n', '    f.integrate(i)\n', '```\n', '\n', "Now let's step through this:\n", '\n', '```\n', 'define start\n', 'define stop\n', 'define our step size\n', 'do numerical integration\n', '```\n'], article)
    
        for style in ["bold_italics", "bold", "italics", "strikeout"]:
            article.block_data = handle_syntax(article.block_data, markdown_regex_map[style], html_regex_map[style])
            h2_2.block_data = handle_syntax(h2_2.block_data, markdown_regex_map[style], html_regex_map[style])
            
            chunked_body.block_data = handle_syntax(chunked_body.block_data, markdown_regex_map[style], html_regex_map[style])
            chunked_body.children[1].block_data = handle_syntax(chunked_body.children[1].block_data, markdown_regex_map[style], html_regex_map[style])

        for i in range(len(article.block_data)):
            self.assertEqual(article.block_data[i], chunked_body.block_data[i])
        for i in range(len(h2_2.block_data)):
            self.assertEqual(chunked_body.children[1].block_data[i], h2_2.block_data[i])
    
    def test_styling_all_nodes(self):
        lines = [ ]
        with open(test_paths["full_suite"], "r") as file:
            lines = file.readlines()
            
        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        chunked_body = handlers.chopper.chop_body_into_nodes(body)
        
        article = MarkdownNode("article", ['\n', '```\n', '**bold**\n', '*italics*\n', '***bold-italics***\n', '~~strike~~\n', '```\n', '\n'], None)
        h2_1 = MarkdownNode("## Table of Features Implemented", ['\n', '| Feature | Implemented |\n', '| ------- | ----------- |\n', '| Unordered Lists | Yes |\n', '| Ordered Lists | Yes |\n', '| Task Lists | Yes |\n', '| images, internal | Yes |\n', '| images, external | Yes |\n', '| links, internal | Yes |\n', '| links, external | Yes |\n', '| links, embedded | No |\n', '| Tables | Yes |\n', '| Callouts | Yes |\n', '| Code Blocks | Yes |\n', '| Math | No |\n', '\n', '![small banner](/content/small_banner.png)\n'], article)
        h2_2 = MarkdownNode("## This is H2", ['\n', "Here's **some text**.\n", '\n', 'I should **probably** get *some* ***lorem-ipsum*** in here.\n', '\n', '~~TODO: add lorem-ipsum~~\n', '\n', "Here's an [internal link](#this-is-h2) to the same file. And here's an [internal site](/Example2.md) link. Here's a [link](/Example2.md#other-h2) to a header in the other file.\n", '\n', "Now for the tricky part (?) let's link to the formatting [sheet](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax). And now an external image: ![Engelbart](https://history-computer.com/ModernComputer/Basis/images/Engelbart.jpg)\n"], article)
        h3_1 = MarkdownNode("### Lorem Ipsum", ['\n', '> [!note] \n', '> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper eros at maximus porta. Vestibulum lectus metus, ornare nec suscipit at, sagittis vitae augue. Vestibulum sem velit, lobortis eu mattis nec, pulvinar ac metus. Nulla ex quam, gravida in efficitur vel, accumsan vitae lorem. In at malesuada mauris. Etiam id dui sit amet nisl efficitur fermentum. Nam mattis sapien eget dolor imperdiet suscipit. Phasellus tristique eleifend dolor nec ultrices. Fusce semper ex mollis risus vehicula fringilla. Vivamus commodo ut tortor vitae ultricies. Mauris consequat fermentum egestas. Nunc pulvinar mauris ipsum, a ornare massa consectetur eget.\n', '\n', 'Donec venenatis rhoncus porttitor. Aliquam sed luctus mi. Fusce vel massa vel magna luctus sollicitudin ut vitae magna. Donec pulvinar consequat nisi, convallis elementum metus condimentum id. Mauris gravida eros non odio varius ornare. Mauris vel orci tincidunt, lobortis augue nec, ultrices lacus. Etiam feugiat sagittis rutrum. Fusce in sapien aliquam, pellentesque risus eu, iaculis est. Nam convallis, mi eget maximus sagittis, justo nisi elementum ex, ut luctus risus mi eu ipsum. Aliquam sit amet egestas diam. Donec non massa ac turpis tempus suscipit.\n', '\n', '> Etiam ultricies massa et placerat placerat. Sed tempus nec metus vel ullamcorper. Vestibulum tempus id mauris in eleifend. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris suscipit tincidunt tellus, in auctor eros laoreet et. Vivamus nisl ligula, facilisis non interdum accumsan, dapibus vel augue. Ut aliquam ligula a dolor lobortis pellentesque. Vivamus nec neque volutpat massa dignissim aliquam sed nec nibh. Nullam vitae ullamcorper est. Morbi condimentum dolor non nisl hendrerit fringilla.\n', '> \n', '> Quisque tempus ipsum eros, non vulputate mauris venenatis eu. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vehicula magna sit amet leo fringilla, non pellentesque ante porta. Integer semper dapibus augue nec accumsan. Duis felis turpis, auctor sit amet lacinia et, tincidunt ac mi. Donec elementum mauris et dictum suscipit. Duis pellentesque augue lectus. Praesent gravida molestie interdum. Vivamus scelerisque erat vel diam efficitur, sit amet mollis urna dapibus. Proin sed fringilla est. Nulla ultricies nisl ut orci eleifend semper. Aliquam eu nulla ligula. Mauris nec fringilla odio. Sed vestibulum purus ut imperdiet rutrum.\n', '\n', 'Curabitur vitae lacus commodo, suscipit dolor tincidunt, tempor orci. Morbi quis erat ligula. Sed arcu eros, sodales ac urna eget, facilisis lobortis tortor. Morbi felis metus, tincidunt eu gravida et, scelerisque dapibus augue. Fusce aliquam condimentum euismod. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas nec porta mi. Curabitur est magna, ultricies non congue id, condimentum sit amet magna. Aenean sagittis purus massa, condimentum gravida lorem auctor eget. \n'], h2_2)
        h3_2 = MarkdownNode("### Lists", ['\n', "Let's see what we're working on for v0.02:\n", '\n', '- task lists\n', '- unordered lists\n', '\t- sub lists\n', '- ordered lists\n', '- use python 3.\n'], h2_2)
        h4_1 = MarkdownNode("#### But in order:", ['\n', '1. unordered lists\n', '\t1. sub lists\n', '2. ordered lists\n', '3. task lists\n'], h3_2)
        hr = MarkdownNode("---", ['\n', "And now let's track our progress:\n", '\n', '- [x] unordered lists\n', '\t- [x] sub lists\n', '- [x] ordered lists\n', '- [ ] task lists\n'], h3_2)
        h2_3 = MarkdownNode("## Now onto some code", ['\n', 'Here, we create a simple loop in python:\n', '\n', '```python\n', '# before: start, stop, step\n', 'for i in range(start, stop, step):\n', '    f.integrate(i)\n', '```\n', '\n', "Now let's step through this:\n", '\n', '```\n', 'define start\n', 'define stop\n', 'define our step size\n', 'do numerical integration\n', '```\n'], article)
    
        styles = list(markdown_regex_map.keys())
        
        for branch in chunked_body.get_branch_name():
            print(branch)
            article_content = article.get_content_for_branch_name(branch)
            body_content = chunked_body.get_content_for_branch_name(branch)
            self.assertEqual(article_content, body_content)
            
            for style in styles:
                article_content = handle_syntax(article_content, markdown_regex_map[style], html_regex_map[style])
                body_content = handle_syntax(body_content, markdown_regex_map[style], html_regex_map[style])
            
            self.assertEqual(len(article_content), len(body_content))
            for i in range(len(article_content)):
                self.assertEqual(article_content[i], body_content[i])
                print(article_content[i], body_content[i])
            print("\n")
            self.assertEqual(article_content, body_content)

    def test_styling_table(self):
        h2_1 = MarkdownNode("## Table of Features Implemented", ['\n', '| Feature | Implemented |\n', '| ------- | ----------- |\n', '| Unordered Lists | Yes |\n', '| Ordered Lists | Yes |\n', '| Task Lists | Yes |\n', '| images, internal | Yes |\n', '| images, external | Yes |\n', '| links, internal | Yes |\n', '| links, external | Yes |\n', '| links, embedded | No |\n', '| Tables | Yes |\n', '| Callouts | Yes |\n', '| Code Blocks | Yes |\n', '| Math | No |\n', '\n', '![small banner](/content/small_banner.png)\n'], None)
        table_content = handlers.formatter.handle_tables(h2_1.block_data)
        print(table_content)

    def test_styling_callout(self):
        """_summary_
        """
        lines = [ ]
        with open(test_paths["full_suite"], "r") as file:
            lines = file.readlines()

        frontmatter, body = handlers.chopper.separate_frontmatter_from_body(lines)
        chunked_body = handlers.chopper.chop_body_into_nodes(body)

        article = MarkdownNode("article", ['\n', '```\n', '**bold**\n', '*italics*\n', '***bold-italics***\n', '~~strike~~\n', '```\n', '\n'], None)
        h2_1 = MarkdownNode("## Table of Features Implemented", ['\n', '| Feature | Implemented |\n', '| ------- | ----------- |\n', '| Unordered Lists | Yes |\n', '| Ordered Lists | Yes |\n', '| Task Lists | Yes |\n', '| images, internal | Yes |\n', '| images, external | Yes |\n', '| links, internal | Yes |\n', '| links, external | Yes |\n', '| links, embedded | No |\n', '| Tables | Yes |\n', '| Callouts | Yes |\n', '| Code Blocks | Yes |\n', '| Math | No |\n', '\n', '![small banner](/content/small_banner.png)\n'], article)
        h2_2 = MarkdownNode("## This is H2", ['\n', "Here's **some text**.\n", '\n', 'I should **probably** get *some* ***lorem-ipsum*** in here.\n', '\n', '~~TODO: add lorem-ipsum~~\n', '\n', "Here's an [internal link](#this-is-h2) to the same file. And here's an [internal site](/Example2.md) link. Here's a [link](/Example2.md#other-h2) to a header in the other file.\n", '\n', "Now for the tricky part (?) let's link to the formatting [sheet](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax). And now an external image: ![Engelbart](https://history-computer.com/ModernComputer/Basis/images/Engelbart.jpg)\n"], article)
        h3_1 = MarkdownNode("### Lorem Ipsum", ['\n', '> [!note] \n', '> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper eros at maximus porta. Vestibulum lectus metus, ornare nec suscipit at, sagittis vitae augue. Vestibulum sem velit, lobortis eu mattis nec, pulvinar ac metus. Nulla ex quam, gravida in efficitur vel, accumsan vitae lorem. In at malesuada mauris. Etiam id dui sit amet nisl efficitur fermentum. Nam mattis sapien eget dolor imperdiet suscipit. Phasellus tristique eleifend dolor nec ultrices. Fusce semper ex mollis risus vehicula fringilla. Vivamus commodo ut tortor vitae ultricies. Mauris consequat fermentum egestas. Nunc pulvinar mauris ipsum, a ornare massa consectetur eget.\n', '\n', 'Donec venenatis rhoncus porttitor. Aliquam sed luctus mi. Fusce vel massa vel magna luctus sollicitudin ut vitae magna. Donec pulvinar consequat nisi, convallis elementum metus condimentum id. Mauris gravida eros non odio varius ornare. Mauris vel orci tincidunt, lobortis augue nec, ultrices lacus. Etiam feugiat sagittis rutrum. Fusce in sapien aliquam, pellentesque risus eu, iaculis est. Nam convallis, mi eget maximus sagittis, justo nisi elementum ex, ut luctus risus mi eu ipsum. Aliquam sit amet egestas diam. Donec non massa ac turpis tempus suscipit.\n', '\n', '> Etiam ultricies massa et placerat placerat. Sed tempus nec metus vel ullamcorper. Vestibulum tempus id mauris in eleifend. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris suscipit tincidunt tellus, in auctor eros laoreet et. Vivamus nisl ligula, facilisis non interdum accumsan, dapibus vel augue. Ut aliquam ligula a dolor lobortis pellentesque. Vivamus nec neque volutpat massa dignissim aliquam sed nec nibh. Nullam vitae ullamcorper est. Morbi condimentum dolor non nisl hendrerit fringilla.\n', '> \n', '> Quisque tempus ipsum eros, non vulputate mauris venenatis eu. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vehicula magna sit amet leo fringilla, non pellentesque ante porta. Integer semper dapibus augue nec accumsan. Duis felis turpis, auctor sit amet lacinia et, tincidunt ac mi. Donec elementum mauris et dictum suscipit. Duis pellentesque augue lectus. Praesent gravida molestie interdum. Vivamus scelerisque erat vel diam efficitur, sit amet mollis urna dapibus. Proin sed fringilla est. Nulla ultricies nisl ut orci eleifend semper. Aliquam eu nulla ligula. Mauris nec fringilla odio. Sed vestibulum purus ut imperdiet rutrum.\n', '\n', 'Curabitur vitae lacus commodo, suscipit dolor tincidunt, tempor orci. Morbi quis erat ligula. Sed arcu eros, sodales ac urna eget, facilisis lobortis tortor. Morbi felis metus, tincidunt eu gravida et, scelerisque dapibus augue. Fusce aliquam condimentum euismod. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas nec porta mi. Curabitur est magna, ultricies non congue id, condimentum sit amet magna. Aenean sagittis purus massa, condimentum gravida lorem auctor eget. \n'], h2_2)
        h3_2 = MarkdownNode("### Lists", ['\n', "Let's see what we're working on for v0.02:\n", '\n', '- task lists\n', '- unordered lists\n', '\t- sub lists\n', '- ordered lists\n', '- use python 3.\n'], h2_2)
        h4_1 = MarkdownNode("#### But in order:", ['\n', '1. unordered lists\n', '\t1. sub lists\n', '2. ordered lists\n', '3. task lists\n'], h3_2)
        hr = MarkdownNode("---", ['\n', "And now let's track our progress:\n", '\n', '- [x] unordered lists\n', '\t- [x] sub lists\n', '- [x] ordered lists\n', '- [ ] task lists\n'], h3_2)
        h2_3 = MarkdownNode("## Now onto some code", ['\n', 'Here, we create a simple loop in python:\n', '\n', '```python\n', '# before: start, stop, step\n', 'for i in range(start, stop, step):\n', '    f.integrate(i)\n', '```\n', '\n', "Now let's step through this:\n", '\n', '```\n', 'define start\n', 'define stop\n', 'define our step size\n', 'do numerical integration\n', '```\n'], article)

        for branch in chunked_body.get_branch_name():
            print(branch)
            article_content = article.get_content_for_branch_name(branch)
            body_content = chunked_body.get_content_for_branch_name(branch)
            self.assertEqual(article_content, body_content)

            article_content = handlers.formatter.handle_callouts(article_content)
            body_content = handlers.formatter.handle_callouts(body_content)

            for art, bod in zip(article_content, body_content):
                self.assertEqual(art, bod)
            print(article_content, body_content)
