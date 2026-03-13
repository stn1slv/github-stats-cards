import re

with open("src/github/fetcher.py", "r") as f:
    content = f.read()

# Replace client = GitHubClient(config.token)
# with with GitHubClient(config.token) as client:
# and indent everything until the return statement

def fix_fetch_user_stats(text):
    lines = text.split('\n')
    out_lines = []
    in_func = False
    in_with = False
    for line in lines:
        if line.startswith('def fetch_user_stats('):
            in_func = True
            out_lines.append(line)
            continue
            
        if in_func:
            if 'client = GitHubClient(config.token)' in line:
                out_lines.append(line.replace('client = GitHubClient(config.token)', 'with GitHubClient(config.token) as client:'))
                in_with = True
                continue
            
            if in_with:
                if line.strip() == '' or line.startswith(' ' * 4):
                    if line.strip() == '':
                        out_lines.append(line)
                    else:
                        out_lines.append('    ' + line)
                else:
                    out_lines.append(line)
                    if not line.startswith(' '):
                        in_func = False
                        in_with = False
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)
    return '\n'.join(out_lines)

new_content = fix_fetch_user_stats(content)
with open("src/github/fetcher.py", "w") as f:
    f.write(new_content)

with open("src/github/langs_fetcher.py", "r") as f:
    langs_content = f.read()

def fix_langs_fetcher(text):
    lines = text.split('\n')
    out_lines = []
    in_func = False
    in_with = False
    for line in lines:
        if line.startswith('def fetch_top_languages('):
            in_func = True
            out_lines.append(line)
            continue
            
        if in_func:
            if 'client = GitHubClient(config.token)' in line:
                out_lines.append(line.replace('client = GitHubClient(config.token)', 'with GitHubClient(config.token) as client:'))
                in_with = True
                continue
            
            if in_with:
                if line.strip() == '' or line.startswith(' ' * 4):
                    if line.strip() == '':
                        out_lines.append(line)
                    else:
                        out_lines.append('    ' + line)
                else:
                    out_lines.append(line)
                    if not line.startswith(' '):
                        in_func = False
                        in_with = False
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)
    return '\n'.join(out_lines)

new_langs = fix_langs_fetcher(langs_content)
with open("src/github/langs_fetcher.py", "w") as f:
    f.write(new_langs)

