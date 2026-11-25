# -*- coding: utf-8 -*-
"""
光電融合デッキのビルド

    python build.py                 … p01〜p10 を結合して ../光電融合.html を書き出す
    python build.py p01_intro       … そのパートだけ ../_preview.html に書き出す（確認用）

スライドの元：docs_光電融合/scenario_本文のみ.md
画像：../img/img01.png 〜 img28.png（HTMLと同じ階層）（docs_光電融合/部材画像 からのコピー。加工しない）
CSS：keizai-slide スキルの style.css ＋ deck.css（この企画の追加分だけ）
"""
import os, sys, io, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_CSS = os.path.expanduser(r"~/.claude/skills/keizai-slide/assets/style.css")

PARTS = [
    "p01_intro", "p02_tema", "p03_tsukurikata", "p04_3sha", "p05_junban",
    "p06_eu_china", "p07_okane", "p08_meibo", "p09_mochikata", "p10_imi",
]


def read(path):
    return io.open(path, encoding="utf-8").read()


def main():
    args = sys.argv[1:]
    if args:
        parts, out = args, os.path.join(HERE, "..", "_preview.html")
    else:
        parts, out = PARTS, os.path.join(HERE, "..", u"光電融合.html")

    css = read(SKILL_CSS) + "\n" + read(os.path.join(HERE, "deck.css"))

    body, used, missing = [], 0, []
    for name in parts:
        p = os.path.join(HERE, name + ".html")
        if not os.path.exists(p):
            missing.append(name)
            continue
        html = read(p)
        used += len(re.findall(r'<section class="slide', html))
        body.append(u"<!-- ========== %s ========== -->\n%s" % (name, html.rstrip()))

    doc = u"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>光電融合</title>
<style>
%s
</style>
</head>
<body>

%s

</body>
</html>
""" % (css, u"\n\n".join(body))

    io.open(out, "w", encoding="utf-8").write(doc)
    print(u"→ %s" % os.path.normpath(out))
    print(u"   スライド %d 枚 / パート %d 本" % (used, len(parts) - len(missing)))
    if missing:
        print(u"   未作成: %s" % u", ".join(missing))

    # 画像の参照チェック（_parts/img にあるか・昇順か）
    nums = [int(n) for n in re.findall(r'img/img(\d\d)\.png', u"\n".join(body))]
    if nums:
        ok = nums == sorted(nums) and len(nums) == len(set(nums))
        print(u"   画像 %d 枚 %s %s" % (len(nums), nums, u"昇順OK" if ok else u"★順番か重複に問題"))
        for n in nums:
            f = os.path.join(HERE, "..", "img", "img%02d.png" % n)
            if not os.path.exists(f):
                print(u"   ★ 画像が無い: img%02d.png" % n)


if __name__ == "__main__":
    main()
