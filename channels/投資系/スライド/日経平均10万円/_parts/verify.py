# -*- coding: utf-8 -*-
"""PLAN.md §8 の検収を機械で回す。 python verify.py"""
import os, io, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "..", "日経平均10万円.html")
SRC = os.path.join(HERE, "..", "..", "..", "docs_日経平均10万円", "scenario_本文のみ.md")

html = io.open(DECK, encoding="utf-8").read()
text = re.sub(r"<[^>]+>", " ", html.split("</style>")[-1])
flat = re.sub(r"<[^>]+>", "", html.split("</style>")[-1])  # タグを詰めて消した版（1兆596億円のように span で割れる数値用）
body = io.open(SRC, encoding="utf-8").read()

ok, ng = [], []


def check(label, cond, detail=""):
    (ok if cond else ng).append(label + (("  → " + detail) if detail and not cond else ""))


n = len(re.findall(r'<section class="slide', html))
check("320枚ある", n == 320, "%d枚" % n)

png = os.path.join(HERE, "..", "PNG")
npng = len([f for f in os.listdir(png) if f.endswith(".png")]) if os.path.isdir(png) else 0
check("PNGが320枚", npng == 320, "%d枚" % npng)

# --- 本文との一致：主要な数値がスライドに乗っているか
nums = ["1兆596億円", "60.4", "77.8", "2.7倍", "206.5", "1.1", "6.8", "562",
        "0.4", "1.2", "26", "1,707", "871", "2兆3,540", "110", "28",
        "1.38", "5.99", "22.87", "4,400", "7.7", "3.8", "11.0", "19.2",
        "14万6,000", "1,657", "77.1", "701", "88", "72", "14.3", "7.8",
        "12.3", "8.9", "1,102", "85.0", "10.7", "4.9", "18.2", "15.7",
        "4,925", "14.94", "7,777", "18.75", "21.59", "2,779", "2.06",
        "8.31", "4.09", "2,713", "6104", "6370", "6368", "2637"]
miss = [x for x in nums if x not in text and x not in flat]
check("主要な数値がすべてスライドにある", not miss, "欠け: " + ", ".join(miss))

# --- ルール
clean = text
for w in ("会社四季報", "子会社", "親会社", "証券会社", "調査会社"):
    clean = clean.replace(w, "")
check("「会社」が無い（四季報等を除く）", "会社" not in clean)
check("割安・買い場・狙い目が無い", not re.search(r"割安|買い場|狙い目|ねらい目|仕込み", text))
check("「〜のです」が無い", not re.search(r"[^も]のです", text))
check("一人称「私」が無い", "私" not in text)
check("番号の点呼が無い", not re.search(r"[1-3１-３]つ目[。、]", text))
check("「本業の利益」が無い", "本業の利益" not in text)
check("米ETFのティッカーが無い", not re.search(r"PIO|FIW", text))
check("チャンネル名を書いていない", 'class="brand"></span>' in html and "インフレ時代" not in text)
check("相対的な時間表現が無い", not re.search(r"先週|今週|今月|先月|昨日", text))

# --- ネタバレ：10万円の距離・4つの数字は、初出より前に出ていない
pos_4wariha = text.find("4割半")
pos_s10 = text.find("Section 10")
check("「4割半」は⑪より前に出ていない", pos_4wariha > pos_s10 > 0,
      "4割半=%d / Section10=%d" % (pos_4wariha, pos_s10))
pos_4tsu = text.find("追うのは、4つだけ")
pos_s11 = text.find("Section 11")
check("「追うのは4つだけ」は⑫が初出", pos_4tsu > pos_s11 > 0)

# --- 新しい型の枚数
check("lagline が6枚以上に出る", len(re.findall(r'class="lagline"', html)) >= 6,
      "%d枚" % len(re.findall(r'class="lagline"', html)))
check("fourcheck が4枚以上に出る", len(re.findall(r'class="fourcheck"', html)) >= 4,
      "%d枚" % len(re.findall(r'class="fourcheck"', html)))
check("lagline の枠が6つずつ", all(c == 6 for c in
      [len(re.findall(r'class="lg', b)) for b in re.findall(r'<div class="lagline">(.*?)</div>\s*<div class="lag-note"', html, re.S)]))

# --- レイアウト
check("t-fx はすべて numviz 付き",
      not re.search(r'class="slide t-fx"', html))
check("t-agenda は3行まで",
      all(len(re.findall(r'class="row"', b)) <= 3
          for b in re.findall(r'<section class="slide t-agenda">(.*?)</section>', html, re.S)))
# 証券コードは「社名カード（初出）」と「株価スライドのラベル」の2か所まで。
# 3社を並べる決算日の表には出さない（コードまで並べると点呼になる）
check("証券コードが点呼になっていない",
      text.count("6104") <= 2 and text.count("6370") <= 3 and text.count("6368") <= 3,
      "6104=%d 6370=%d 6368=%d" % (text.count("6104"), text.count("6370"), text.count("6368")))

print("＝＝ 合格 %d 件 ＝＝" % len(ok))
for s in ok:
    print("  ○", s)
if ng:
    print("\n＝＝ 要確認 %d 件 ＝＝" % len(ng))
    for s in ng:
        print("  ×", s)
else:
    print("\n要確認なし。")
