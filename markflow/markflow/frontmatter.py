import re
import yaml

def extract_frontmatter(text):
    if not text.startswith('---'):
        return {}, text
    # Fixed regex to accept \r\n as well
    # Added ? to make the whole middle part optional, handling empty frontmatter correctly
    match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', text, re.DOTALL)
    if not match:
        # Check for empty frontmatter explicitly
        match = re.match(r'^---\r?\n---\r?\n', text)
        if match:
            return {}, text[match.end():]
        return {}, text
    yaml_str = match.group(1)
    if not yaml_str.strip():
        frontmatter = {}
    else:
        frontmatter = yaml.safe_load(yaml_str) or {}
    remaining = text[match.end():]
    return frontmatter, remaining
