import re

def process_shortcodes(text):
    # Protect code blocks by replacing them with placeholders
    code_blocks = []
    def protect_code(match):
        code_blocks.append(match.group(0))
        return f"%%CODEBLOCK{len(code_blocks)-1}%%"
    text = re.sub(r'```[^`]*```', protect_code, text, flags=re.DOTALL)

    def replace_youtube(match):
        video_id = match.group(1).strip()
        # Ensure we use exactly the format expected by the test
        return f'<iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
    text = re.sub(r'\{\{youtube\s+(.*?)\}\}', replace_youtube, text)

    # Restore code blocks
    for i, block in enumerate(code_blocks):
        text = text.replace(f'%%CODEBLOCK{i}%%', block)
    return text
