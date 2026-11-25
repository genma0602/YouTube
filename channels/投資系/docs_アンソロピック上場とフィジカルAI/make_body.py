# -*- coding: utf-8 -*-
# scenario_draft.md → scenario_本文のみ.md / .txt（注記・区切り線・表を除いた本文だけ）。G7財政危機の make_body.py と同じ
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = r"C:\Users\genki\01_YouTube\channels\投資系\docs_アンソロピック上場とフィジカルAI"
SRC = D + r"\scenario_draft.md"
TITLE = "Anthropic上場とフィジカルAI。日本の腕周りの5社（仮）"

lines = io.open(SRC, encoding='utf-8').read().split('\n')
md = ["# " + TITLE, ""]
started = False
for ln in lines:
    s = ln.rstrip()
    if s.startswith('## '):
        started = True
        md.append(s); md.append(""); continue
    if not started:
        continue
    if s.startswith('>') or s.startswith('---') or s.startswith('|') or s.startswith('# '):
        continue
    if s.strip() == "":
        continue
    md.append(s); md.append("")
out = []
for s in md:
    if s == "" and out and out[-1] == "":
        continue
    out.append(s)
md_text = '\n'.join(out).rstrip('\n') + '\n'
io.open(D + r"\scenario_本文のみ.md", 'w', encoding='utf-8', newline='\n').write(md_text)

txt = []
for s in out:
    if s.startswith('# '): txt.append(s[2:])
    elif s.startswith('## '): txt.append(s[3:])
    elif s.startswith('### '): txt.append(s[4:])
    else: txt.append(s)
io.open(D + r"\scenario_本文のみ.txt", 'w', encoding='utf-8', newline='\n').write('\n'.join(txt).rstrip('\n') + '\n')

body = ''.join(s for s in out if not s.startswith('#'))
print('本文字数（見出し除く）', len(re.sub(r'\s', '', body)), '/ 見出し', sum(1 for s in out if s.startswith('## ')), '/ 小見出し', sum(1 for s in out if s.startswith('### ')))
print('残った > や | の行:', sum(1 for s in out if s.startswith('>') or s.startswith('|')))
