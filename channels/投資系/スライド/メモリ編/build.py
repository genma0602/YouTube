# -*- coding: utf-8 -*-
"""
_parts/*.html を連結して 1本のスライドHTMLを組み立てる。

  python build.py

_parts/_style.html … 前作から引き継いだ <style>（デザインは再発明しない）
_parts/01.html 〜 11.html … 台本の①〜⑪に対応するスライド群

出力: AI半導体はまだ序章.html
"""
import os, glob, io, re

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, "_parts")
TITLE = "AI半導体はまだ序章｜メモリと日本"
OUT = os.path.join(HERE, "AI半導体はまだ序章.html")

def main():
    style = io.open(os.path.join(PARTS, "_style.html"), encoding="utf-8").read()

    files = sorted(f for f in glob.glob(os.path.join(PARTS, "*.html"))
                   if not os.path.basename(f).startswith("_"))
    if not files:
        raise SystemExit("_parts/ にスライドのHTMLがありません。")

    body, counts = [], []
    for f in files:
        src = io.open(f, encoding="utf-8").read()
        n = len(re.findall(r'<section class="slide', src))
        counts.append((os.path.basename(f), n))
        body.append(src.rstrip())

    html = (
        "<!DOCTYPE html>\n<html lang=\"ja\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{TITLE}</title>\n{style}\n</head>\n<body>\n"
        + "\n\n".join(body)
        + "\n</body>\n</html>\n"
    )
    io.open(OUT, "w", encoding="utf-8").write(html)

    total = 0
    start = 1
    for name, n in counts:
        print(f"  {name}: {n:3d} 枚  (slide_{start:03d} 〜 slide_{start+n-1:03d})")
        start += n
        total += n
    print(f"→ {OUT}")
    print(f"合計 {total} 枚")

if __name__ == "__main__":
    main()
