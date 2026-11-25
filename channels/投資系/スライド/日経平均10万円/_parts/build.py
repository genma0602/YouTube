# -*- coding: utf-8 -*-
"""
日経平均10万円（マクロ編）デッキのビルド

    python build.py                     … p01〜p15 を結合して ../日経平均10万円.html を書き出す
    python build.py p05_shibaura        … そのパートだけ ../_preview.html に書き出す（確認用）

スライドの元：docs_日経平均10万円/scenario_本文のみ.md（20,731字）
構成プラン：../PLAN.md（320枚）
CSS：keizai-slide スキルの style.css ＋ deck.css（この企画の追加分だけ）
"""
import os, sys, io, re

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_CSS = os.path.expanduser(r"~/.claude/skills/keizai-slide/assets/style.css")

PARTS = [
    "p01_yumemonogatari", "p02_30nen", "p03_seifu", "p04_chumon", "p05_shibaura",
    "p06_shakkin", "p07_toushi", "p08_kyuryo", "p09_naze_nihon", "p10_taiwan",
    "p11_kotaeawase", "p12_miru_suuji", "p13_mizu", "p14_nisa", "p15_shime",
]

# PLAN.md §1 の枚数（ずれたら警告を出す）
PLANNED = {
    "p01_yumemonogatari": 14, "p02_30nen": 19, "p03_seifu": 15, "p04_chumon": 18,
    "p05_shibaura": 36, "p06_shakkin": 19, "p07_toushi": 22, "p08_kyuryo": 12,
    "p09_naze_nihon": 36, "p10_taiwan": 15, "p11_kotaeawase": 16,
    "p12_miru_suuji": 16, "p13_mizu": 52, "p14_nisa": 18, "p15_shime": 12,
}


def read(path):
    return io.open(path, encoding="utf-8").read()


def main():
    args = sys.argv[1:]
    if args:
        parts, out = args, os.path.join(HERE, "..", "_preview.html")
    else:
        parts, out = PARTS, os.path.join(HERE, "..", u"日経平均10万円.html")

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
        print(u"   %-20s %3d 枚%s" % (name, n, flag))
        body.append(u"<!-- ========== %s（%d枚） ========== -->\n%s" % (name, n, html.rstrip()))

    doc = u"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>日経平均10万円</title>
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
    clean = text.replace(u"会社四季報", u"").replace(u"子会社", u"").replace(u"親会社", u"").replace(u"証券会社", u"").replace(u"調査会社", u"")
    ng = {
        u"「会社」": len(re.findall(u"会社", clean)),
        u"割安・買い場・狙い目": len(re.findall(u"割安|買い場|狙い目|ねらい目|仕込み", text)),
        u"〜のです": len(re.findall(u"[^も]のです", text)),
        u"私": len(re.findall(u"私", text)),
        u"番号の点呼": len(re.findall(u"[1-3１-３]つ目[。、]", text)),
        u"本業の利益": len(re.findall(u"本業の利益", text)),
        u"米ETFのティッカー": len(re.findall(u"PIO|FIW", text)),
    }
    hit = [u"%s %d件" % (k, v) for k, v in ng.items() if v]
    print(u"   禁止語チェック: %s" % (u" / ".join(hit) if hit else u"すべて0件"))


if __name__ == "__main__":
    main()
