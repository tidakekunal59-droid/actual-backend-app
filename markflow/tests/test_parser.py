import pytest
from markflow.parser import parse_markdown

def test_heading():
    blocks = parse_markdown("# Hello")
    assert blocks[0] == ('heading', 1, 'Hello')

def test_heading_level_two():
    blocks = parse_markdown("## Section")
    assert blocks[0] == ('heading', 2, 'Section')

def test_heading_level_six():
    blocks = parse_markdown("###### Deep")
    assert blocks[0] == ('heading', 6, 'Deep')

def test_multiple_headings():
    text = "# Title\n## Section\nContent"
    blocks = parse_markdown(text)
    assert len(blocks) == 3
    assert blocks[0] == ('heading', 1, 'Title')
    assert blocks[1] == ('heading', 2, 'Section')
    assert blocks[2][0] == 'paragraph'

def test_unordered_list():
    text = "- item1\n- item2"
    blocks = parse_markdown(text)
    assert blocks[0] == ('list', ['item1', 'item2'])

def test_list_with_asterisk():
    md = "* item1\n* item2"
    blocks = parse_markdown(md)
    assert blocks[0] == ('list', ['item1', 'item2'])

def test_list_mixed_separators():
    md = "- item1\n* item2"
    blocks = parse_markdown(md)
    assert blocks[0] == ('list', ['item1', 'item2'])

def test_code_block():
    text = "```python\nprint('hello')\n```"
    blocks = parse_markdown(text)
    assert blocks[0] == ('code', 'python', "print('hello')")

def test_code_block_without_language():
    md = "```\nplain text\n```"
    blocks = parse_markdown(md)
    assert blocks[0] == ('code', '', 'plain text')

def test_multiple_code_blocks():
    md = "```py\na\n```\n\n```py\nb\n```"
    blocks = parse_markdown(md)
    assert len(blocks) == 2
    assert blocks[0] == ('code', 'py', 'a')
    assert blocks[1] == ('code', 'py', 'b')

def test_paragraph_spanning_multiple_lines():
    md = "Line1\nLine2\nLine3"
    blocks = parse_markdown(md)
    assert blocks[0] == ('paragraph', 'Line1\nLine2\nLine3')

def test_empty_document():
    assert parse_markdown("") == []

def test_empty_lines_between_blocks():
    md = "# Header\n\nContent"
    blocks = parse_markdown(md)
    assert len(blocks) == 2
    assert blocks[0][0] == 'heading'
    assert blocks[1][0] == 'paragraph'
