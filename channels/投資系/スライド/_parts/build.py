# -*- coding: utf-8 -*-
"""パーツHTMLを結合して、完成デッキを書き出す。"""
import io, os, glob, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(os.path.dirname(BASE), 'AI半導体バブル2026', 'AI半導体バブルは終わったのか.html')
CSS  = r'C:/Users/genki/.claude/skills/keizai-slide/assets/style.css'

css = io.open(CSS, encoding='utf-8').read()
parts = sorted(glob.glob(os.path.join(BASE, 'p*.html')))

body = []
for p in parts:
    body.append(io.open(p, encoding='utf-8').read().strip())

html = (
    '<!DOCTYPE html>\n<html lang="ja"><head><meta charset="UTF-8">\n'
    '<title>AI半導体バブルは終わったのか</title>\n<style>\n'
    + css +
    '\n</style></head><body>\n'
    + '\n\n'.join(body) +
    '\n</body></html>\n'
)
io.open(OUT, 'w', encoding='utf-8').write(html)

n = len(re.findall(r'<section class="slide', html))
print('パーツ:', len(parts))
for p in parts:
    c = len(re.findall(r'<section class="slide', io.open(p, encoding='utf-8').read()))
    print('  %-28s %3d 枚' % (os.path.basename(p), c))
print('合計:', n, '枚 ->', OUT)
