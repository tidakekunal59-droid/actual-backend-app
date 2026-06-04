from markflow.shortcodes import process_shortcodes

def test_youtube_shortcode():
    text = "Watch {{youtube dQw4w9WgXcQ}} now"
    result = process_shortcodes(text)
    assert 'iframe' in result
    assert 'dQw4w9WgXcQ' in result

def test_multiple_shortcodes():
    text = "{{youtube aaa}} and {{youtube bbb}}"
    result = process_shortcodes(text)
    assert 'youtube.com/embed/aaa' in result
    assert 'youtube.com/embed/bbb' in result

def test_shortcode_with_spaces():
    text = "{{youtube    dQw4w9WgXcQ   }}"
    result = process_shortcodes(text)
    assert 'dQw4w9WgXcQ' in result

def test_no_shortcode_returns_original():
    text = "Just normal text"
    result = process_shortcodes(text)
    assert result == text

def test_shortcode_adjacent_to_text():
    text = "start{{youtube xyz}}end"
    result = process_shortcodes(text)
    assert 'start<iframe' in result
    assert 'end' in result

def test_shortcode_in_code_block_not_replaced():
    # This test will FAIL initially (intentional bug)
    text = "```\n{{youtube xyz}}\n```"
    result = process_shortcodes(text)
    assert 'iframe' not in result, "Shortcode inside code block should not be processed"
