# -*- coding: utf-8 -*-
"""パーツHTMLを結合して、完成デッキを書き出す。

  python _parts/build.py

_parts/p01_*.html 〜 p11_*.html … 台本の①〜⑪に対応
CSS は keizai-slide スキルの style.css を直読み（デザインは再発明しない）
"""
import io, os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(os.path.dirname(BASE), '日米同時利上げ.html')
CSS  = r'C:/Users/genki/.claude/skills/keizai-slide/assets/style.css'
TITLE = '半世紀ぶりの日米同時利上げ'

css = io.open(CSS, encoding='utf-8').read()
parts = sorted(glob.glob(os.path.join(BASE, 'p*.html')))
if not parts:
    raise SystemExit('_parts/ にスライドのHTMLがありません。')

body = [io.open(p, encoding='utf-8').read().strip() for p in parts]

html = (
    '<!DOCTYPE html>\n<html lang="ja"><head><meta charset="UTF-8">\n'
    f'<title>{TITLE}</title>\n<style>\n'
    + css +
    '\n</style></head><body>\n'
    + '\n\n'.join(body) +
    '\n</body></html>\n'
)
io.open(OUT, 'w', encoding='utf-8').write(html)

start, total = 1, 0
for p in parts:
    c = len(re.findall(r'<section class="slide', io.open(p, encoding='utf-8').read()))
    print('  %-24s %3d 枚  (slide_%03d 〜 slide_%03d)' % (os.path.basename(p), c, start, start + c - 1))
    start += c; total += c
print('合計:', total, '枚 ->', OUT)
