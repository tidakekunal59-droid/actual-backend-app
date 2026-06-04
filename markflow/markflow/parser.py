import re

def parse_markdown(text: str):
    """Parse Markdown text into a list of block tokens."""
    lines = text.split('\n')
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('#'):
            level = len(line.split(' ')[0])
            content = line[level:].strip()
            blocks.append(('heading', level, content))
            i += 1
        elif line.startswith('```'):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append(('code', lang, '\n'.join(code_lines)))
            i += 1  # skip closing ```
        elif line.startswith('- ') or line.startswith('* '):
            items = []
            while i < len(lines) and (lines[i].startswith('- ') or lines[i].startswith('* ')):
                items.append(lines[i][2:].strip())
                i += 1
            blocks.append(('list', items))
        elif line.strip() == '':
            i += 1
        else:
            para = line
            i += 1
            while i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('#') and not lines[i].startswith('```') and not lines[i].startswith('- ') and not lines[i].startswith('* '):
                para += '\n' + lines[i]
                i += 1
            blocks.append(('paragraph', para))
    return blocks
