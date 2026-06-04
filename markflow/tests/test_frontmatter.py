from markflow.frontmatter import extract_frontmatter

def test_no_frontmatter():
    fm, text = extract_frontmatter("Hello")
    assert fm == {}
    assert text == "Hello"

def test_basic_frontmatter():
    md = "---\ntitle: Hello\n---\nContent"
    fm, remaining = extract_frontmatter(md)
    assert fm == {"title": "Hello"}
    assert remaining == "Content"

def test_frontmatter_with_multiple_keys():
    md = "---\ntitle: Hello\nauthor: John\n---\nContent"
    fm, remaining = extract_frontmatter(md)
    assert fm == {"title": "Hello", "author": "John"}
    assert remaining == "Content"

def test_frontmatter_with_list_value():
    md = "---\ntags:\n  - a\n  - b\n---\nContent"
    fm, _ = extract_frontmatter(md)
    assert fm == {"tags": ["a", "b"]}

def test_no_closing_dashes():
    md = "---\ntitle: Hello\nContent"
    fm, remaining = extract_frontmatter(md)
    assert fm == {}
    assert remaining == md

def test_empty_frontmatter():
    md = "---\n---\nContent"
    fm, remaining = extract_frontmatter(md)
    assert fm == {}
    assert remaining == "Content"

def test_frontmatter_with_crlf():
    # This test will FAIL initially (intentional bug)
    md = "---\r\ntitle: Hello\r\n---\r\nContent"
    fm, remaining = extract_frontmatter(md)
    assert fm == {"title": "Hello"}
    assert remaining == "Content"
