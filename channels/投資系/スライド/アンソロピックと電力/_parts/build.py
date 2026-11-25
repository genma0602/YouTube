# -*- coding: utf-8 -*-
"""
アンソロピックと電力・デッキのビルド

    python build.py                 … p01〜p19 を結合して ../サイバーセキュリティ.html を書き出す
    python build.py p01_intro       … そのパートだけ ../_preview.html に書き出す（確認用）

スライドの元：docs_アンソロピックと電力/scenario_本文のみ.md（24,734字）
構成プラン：../PLAN.md（375枚）
CSS：keizai-slide スキルの style.css ＋ deck.css（この企画の追加分だけ）
"""
import os, sys, io, re

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_CSS = os.path.expanduser(r"~/.claude/skills/keizai-slide/assets/style.css")

PARTS = [
    "p01_intro",
    "p02_kasegi",
    "p03_jojo",
    "p04_denki_ryo",
    "p05_mhi",
    "p06_coreweave",
    "p07_kaishu",
    "p08_denki",
    "p09_todokanai",
    "p10_hitachi",
    "p11_meiden",
    "p12_shizuki",
    "p13_jesco",
    "p14_daikin",
    "p15_nihondengi",
    "p16_santec",
    "p17_nisa",
    "p18_kikikata",
    "p19_shime",
]

# PLAN.md §1 の枚数（ずれたら警告を出す）
PLANNED = {
    "p01_intro": 12,
    "p02_kasegi": 16,
    "p03_jojo": 13,
    "p04_denki_ryo": 10,
    "p05_mhi": 40,
    "p06_coreweave": 18,
    "p07_kaishu": 38,
    "p08_denki": 13,
    "p09_todokanai": 14,
    "p10_hitachi": 29,
    "p11_meiden": 22,
    "p12_shizuki": 22,
    "p13_jesco": 22,
    "p14_daikin": 30,
    "p15_nihondengi": 20,
    "p16_santec": 22,
    "p17_nisa": 15,
    "p18_kikikata": 11,
    "p19_shime": 5,
}


def read(path):
    return io.open(path, encoding="utf-8").read()


def main():
    args = sys.argv[1:]
    if args:
        parts, out = args, os.path.join(HERE, "..", "_preview.html")
    else:
        parts, out = PARTS, os.path.join(HERE, "..", u"アンソロピックと電力.html")

    css = read(SKILL_CSS) + "\n" + read(os.path.join(HERE, "deck.css"))

    body, total, missing = [], 0, []
    for name in parts:
        p = os.path.join(HERE, name + ".html")
        if not os.path.exists(p):
            missing.append(name)
            continue
        html = read(p)
        n = len(re.findall(r'<section class="slide', html))
        total += n
        want = PLANNED.get(name)
        flag = u"" if want is None or want == n else u"  ★プランは %d 枚" % want
        print(u"   %-16s %3d 枚%s" % (name, n, flag))
        body.append(u"<!-- ========== %s（%d枚） ========== -->\n%s" % (name, n, html.rstrip()))

    doc = u"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>アンソロピックと電力</title>
<style>
%s
</style>
</head>
<body>

%s

</body>
</html>
""" % (css, u"\n\n".join(body))

    io.open(out, "w", encoding="utf-8", newline="\n").write(doc)
    print(u"→ %s" % os.path.normpath(out))
    print(u"   合計 %d 枚 / パート %d 本" % (total, len(parts) - len(missing)))
    if missing:
        print(u"   未作成: %s" % u", ".join(missing))

    # 禁止語の機械チェック（本文のルールをスライドにも通す）
    text = re.sub(r"<[^>]+>", "", u"\n".join(body))
    ng = {
        u"「会社」": len(re.findall(u"会社", text.replace(u"会社四季報", u"").replace(u"子会社", u"").replace(u"調査会社", u"").replace(u"証券会社", u""))),
        u"割安・買い場・狙い目": len(re.findall(u"割安|買い場|狙い目|ねらい目|仕込み|「買い」|上がります", text)),
        u"〜のです": len(re.findall(u"[^も]のです", text)),
        u"私": len(re.findall(u"私", text)),
        u"実数の騰落率": len(re.findall(u"[+＋][0-9]+[.][0-9]+%", text)),
        u"Nvidia表記": len(re.findall(u"Nvidia", text)),
        u"TWh": len(re.findall(u"TWh", text)),
    }
    hit = [u"%s %d件" % (k, v) for k, v in ng.items() if v]
    print(u"   禁止語チェック: %s" % (u" / ".join(hit) if hit else u"すべて0件"))


if __name__ == "__main__":
    main()
