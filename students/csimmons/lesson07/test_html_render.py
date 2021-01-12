#!/usr/bin/env python3
#Craig Simmons

import io
import pytest
from html_render import *

# utility function for testing render methods
def render_result(element, ind=""):
    outfile = io.StringIO()
    if ind:
        element.render(outfile, ind)
    else:
        element.render(outfile)
    return outfile.getvalue()

def test_init():
    e = Element()
    e = Element("this is some text")

def test_append():
    e = Element("this is some text")
    e.append("some more text")

def test_render_element():
    e = Element("this is some text")
    e.append("and this is some more text")
    file_contents = render_result(e).strip()
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert file_contents.index("this is") < file_contents.index("and this")
    assert file_contents.startswith("<html>")
    assert file_contents.endswith("</html>")
    assert file_contents.count("<html>") == 1
    assert file_contents.count("</html>") == 1
    print(file_contents)

def test_render_element2():
    e = Element()
    e.append("this is some text")
    e.append("and this is some more text")
    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert file_contents.index("this is") < file_contents.index("and this")
    assert file_contents.startswith("<html>")
    assert file_contents.endswith("</html>")
    assert file_contents.count("<html>") == 1
    assert file_contents.count("</html>") == 1

def test_one_line_tag_append():
    e = OneLineTag("The initial one-line content")
    with pytest.raises(NotImplementedError):
        e.append("some more content")
    file_contents = render_result(e).strip()
    print(file_contents)

def test_attributes():
    e = P("A paragraph of text", style="text-align: center", id="intro")
    file_contents = render_result(e).strip()
    print(file_contents)
    assert "A paragraph of text" in file_contents
    assert file_contents.endswith("</p>")
    assert file_contents.startswith("<p")
    assert 'style="text-align: center"' in file_contents
    assert 'id="intro"' in file_contents

def test_html():
    e = Html("this is some text")
    e.append("and this is some more text")
    file_contents = render_result(e).strip()
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert file_contents.index("this is") < file_contents.index("and this")
    assert file_contents.startswith("<html>")
    assert file_contents.endswith("</html>")
    assert file_contents.count("<html>") == 1
    assert file_contents.count("</html>") == 1

def test_head():
    e = Head("this is some text")
    e.append("and this is some more text")
    file_contents = render_result(e).strip()
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert file_contents.count("<head>") == 1
    assert file_contents.count("</head>") == 1

def test_body():
    e = Body("this is some text")
    e.append("and this is some more text")
    file_contents = render_result(e).strip()
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert file_contents.startswith("<body>")
    assert file_contents.endswith("</body>")


def test_p():
    e = P("this is some text")
    e.append("and this is some more text")
    file_contents = render_result(e).strip()
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert file_contents.startswith("<p>")
    assert file_contents.endswith("</p>")

def test_title():
    e = Title("This is a Title")
    file_contents = render_result(e).strip()
    print(file_contents)
    assert "\n" not in file_contents
    assert file_contents.startswith("<title>")
    assert file_contents.endswith("</title>")

def test_sub_element():
    page = Html()
    page.append("some plain text.")
    page.append(P("A simple paragraph of text"))
    page.append("Some more plain text.")

    file_contents = render_result(page)
    print(file_contents) # so we can see it if the test fails

    # note: The previous tests should make sure that the tags are getting
    #       properly rendered, so we don't need to test that here.
    assert "some plain text" in file_contents
    assert "A simple paragraph of text" in file_contents
    assert "Some more plain text." in file_contents
    assert "some plain text" in file_contents
    # but make sure the embedded element's tags get rendered!
    assert "<p>" in file_contents
    assert "</p>" in file_contents




########
# Step 3
########

# Add your tests here!

# #####################
# # indentation testing
# #  Uncomment for Step 9 -- adding indentation
# #####################


# def test_indent():
#     """
#     Tests that the indentation gets passed through to the renderer
#     """
#     html = Html("some content")
#     file_contents = render_result(html, ind="   ").rstrip()  #remove the end newline

#     print(file_contents)
#     lines = file_contents.split("\n")
#     assert lines[0].startswith("   <")
#     print(repr(lines[-1]))
#     assert lines[-1].startswith("   <")


# def test_indent_contents():
#     """
#     The contents in a element should be indented more than the tag
#     by the amount in the indent class attribute
#     """
#     html = Element("some content")
#     file_contents = render_result(html, ind="")

#     print(file_contents)
#     lines = file_contents.split("\n")
#     assert lines[1].startswith(Element.indent)


# def test_multiple_indent():
#     """
#     make sure multiple levels get indented fully
#     """
#     body = Body()
#     body.append(P("some text"))
#     html = Html(body)

#     file_contents = render_result(html)

#     print(file_contents)
#     lines = file_contents.split("\n")
#     for i in range(3):  # this needed to be adapted to the <DOCTYPE> tag
#         assert lines[i + 1].startswith(i * Element.indent + "<")

#     assert lines[4].startswith(3 * Element.indent + "some")


# def test_element_indent1():
#     """
#     Tests whether the Element indents at least simple content

#     we are expecting to to look like this:

#     <html>
#         this is some text
#     <\html>

#     More complex indentation should be tested later.
#     """
#     e = Element("this is some text")

#     # This uses the render_results utility above
#     file_contents = render_result(e).strip()

#     # making sure the content got in there.
#     assert("this is some text") in file_contents

#     # break into lines to check indentation
#     lines = file_contents.split('\n')
#     # making sure the opening and closing tags are right.
#     assert lines[0] == "<html>"
#     # this line should be indented by the amount specified
#     # by the class attribute: "indent"
#     assert lines[1].startswith(Element.indent + "thi")
#     assert lines[2] == "</html>"
#     assert file_contents.endswith("</html>")
