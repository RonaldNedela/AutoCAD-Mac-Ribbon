#!/usr/bin/env python3
import re

with open('ui/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('ui/ribbon.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('ui/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Strip existing <style>...</style> if any
html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)
# Strip existing <link rel="stylesheet" ...> if any
html = re.sub(r'<link\s+rel=["\']stylesheet["\'].*?>', '', html)

# Strip existing <script>...</script> at the bottom or <script src="...">
html = re.sub(r'<script\s+src=["\']ribbon\.js["\']></script>', '', html)
html = re.sub(r'<script>.*?</script>', '', html, flags=re.DOTALL)

# Insert <style> before </head>
style_block = f"<style>\n{css}\n</style>\n</head>"
html = html.replace('</head>', style_block)

# Insert <script> before </body>
script_block = f"<script>\n{js}\n</script>\n</body>"
html = html.replace('</body>', script_block)

with open('ui/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Bundled index.html created. Total bytes:", len(html))
