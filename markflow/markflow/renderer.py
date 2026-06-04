import re

def render_html(blocks):
    html = []
    for block_type, *args in blocks:
        if block_type == 'heading':
            level, content = args
            html.append(f'<h{level}>{_inline_parse(content)}</h{level}>')
        elif block_type == 'paragraph':
            html.append(f'<p>{_inline_parse(args[0])}</p>')
        elif block_type == 'code':
            lang, code = args
            code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html.append(f'<pre><code class="language-{lang}">{code}</code></pre>')
        elif block_type == 'list':
            items = args[0]
            lis = ''.join(f'<li>{_inline_parse(item)}</li>' for item in items)
            html.append(f'<ul>{lis}</ul>')
    return '\n'.join(html)

def _inline_parse(text):
    # bold, italic, and code
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text
