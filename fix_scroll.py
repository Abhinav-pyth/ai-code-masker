import os
import re
import glob

template_dir = r"e:\ai-playground\devtool\ai-code-masker-main\api\templates"
files = glob.glob(os.path.join(template_dir, "*.html"))
exclude = ['base.html', 'index.html', 'tools.html']

for filepath in files:
    filename = os.path.basename(filepath)
    if filename in exclude:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    modified = False

    # FIX 1: Replace 100vh with 100% to stop it fighting the layout
    if 'min-height:100vh' in content or 'min-height: 100vh' in content:
        content = re.sub(r'min-height:\s*100vh', 'min-height: 100%', content)
        modified = True
    
    if 'height:calc(100vh - 72px)' in content:
        content = content.replace('height:calc(100vh - 72px)', 'height: 100%')
        modified = True
        
    if 'height: 100vh' in content:
        content = content.replace('height: 100vh', 'height: 100%')
        modified = True
        
    if 'min-h-screen' in content:
        content = content.replace('min-h-screen', 'min-h-full')
        modified = True

    if 'h-screen' in content:
        # be careful with h-screen, usually better to use h-full
        content = content.replace('h-screen', 'h-full')
        modified = True

    # FIX 2: Ensure the content is wrapped in page-scroll if it's a simple page
    # If the page doesn't have flex-grow on its main container, it probably needs page-scroll
    # Let's check what's right after {% block content %}
    block_match = re.search(r'{%\s*block\s+content\s*%}(.*?){%\s*endblock\s*}', content, re.DOTALL)
    if block_match:
        inner = block_match.group(1).strip()
        # Some simple heuristics to decide if it's a split pane app (has top toolbar + flex-grow split)
        is_split_app = ('border-b border-white/5' in inner and 'flex-grow' in inner) or 'hql_to_sql' in filename or 'api_tester' in filename or 'clinical_parser' in filename
        has_page_scroll = 'class="page-scroll"' in inner
        
        if not is_split_app and not has_page_scroll:
            # Wrap the entire inner content
            new_inner = f'\n<div class="page-scroll flex flex-col">\n{inner}\n</div>\n'
            content = content.replace(block_match.group(1), new_inner)
            modified = True
            
        # If it IS a split app, make sure it has overflow-hidden on its outer container if it doesn't already
        # Specifically for api_tester, clinical_parser, hql_to_sql
        if is_split_app and ('hql_to_sql.html' == filename or 'api_tester.html' == filename or 'clinical_parser.html' == filename):
            pass # We'll do this manually if needed, Python script is for the bulk

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed layout in {filename}")
    else:
        print(f"No changes needed for {filename}")

print("Done")
