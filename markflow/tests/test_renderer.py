from markflow.parser import parse_markdown
from markflow.renderer import render_html

def test_heading_rendering():
    md = "# Hello"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<h1>Hello</h1>' in html

def test_bold_text():
    md = "**bold**"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<strong>bold</strong>' in html

def test_italic_text():
    md = "*italic*"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<em>italic</em>' in html

def test_inline_code():
    md = "use `print()`"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<code>print()</code>' in html

def test_bold_and_italic_together():
    md = "**bold** and *italic*"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<strong>bold</strong>' in html
    assert '<em>italic</em>' in html

def test_nested_bold_inside_italic():
    # known edge case — may not be perfect but ensures no crash
    md = "*italic **bold** text*"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<strong>bold</strong>' in html

def test_code_block_escapes_html():
    md = "```html\n<div>\n```"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '&lt;div&gt;' in html

def test_list_rendering():
    md = "- item1\n- item2"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<ul><li>item1</li><li>item2</li></ul>' in html

def test_empty_list():
    md = "- "
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '<ul><li></li></ul>' in html

def test_paragraph_with_special_chars():
    md = "Price: 5 < 10"
    blocks = parse_markdown(md)
    html = render_html(blocks)
    assert '5 < 10' in html
