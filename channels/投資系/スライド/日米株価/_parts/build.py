# -*- coding: utf-8 -*-
"""
日米株価デッキのビルド

    python build.py              … p01〜p19 を結合して ../日米株価.html を書き出す
    python build.py p06          … そのパートだけ ../_preview.html に書き出す

スライドの元：docs_日米株価/scenario_本文のみ.md（24,114字）
構成プラン：../PLAN.md（370枚）
"""
import os, sys, io, re, importlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SKILL_CSS = os.path.expanduser(r"~/.claude/skills/keizai-slide/assets/style.css")

PLANNED = {"p01": 14, "p02": 11, "p03": 12, "p04": 21, "p05": 13, "p06": 44, "p07": 16, "p08": 16, "p09": 17,
           "p10": 24, "p11": 20, "p12": 10, "p13": 14, "p14": 30, "p15": 32, "p16": 29, "p17": 25, "p18": 18, "p19": 4}
PARTS = sorted(PLANNED)


def read(p):
    return io.open(p, encoding="utf-8").read()


def main():
    args = sys.argv[1:]
    parts = args or PARTS
    out = os.path.join(HERE, "..", "_preview.html" if args else u"日米株価.html")
    css = read(SKILL_CSS) + "\n" + read(os.path.join(HERE, "deck.css"))
    body, total, missing = [], 0, []
    for name in parts:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            missing.append(name); continue
        mod = importlib.import_module(name)
        n = len(mod.S)
        total += n
        want = PLANNED.get(name)
        flag = u"" if want == n else u"  ★プランは %s 枚" % want
        print(u"   %-4s %3d 枚%s" % (name, n, flag))
        body.append(u"<!-- ========== %s（%d枚） ========== -->\n%s" % (name, n, u"\n".join(mod.S)))
    doc = (u'<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<title>日米株価は暴落しない</title>\n'
           u'<style>\n%s\n</style>\n</head>\n<body>\n\n%s\n\n</body>\n</html>\n') % (css, u"\n\n".join(body))
    io.open(out, "w", encoding="utf-8", newline="\n").write(doc)
    print(u"→ %s" % os.path.normpath(out))
    print(u"   合計 %d 枚 / パート %d 本" % (total, len(parts) - len(missing)))
    if missing:
        print(u"   未作成: %s" % u", ".join(missing))
    text = re.sub(r"<[^>]+>", "", u"\n".join(body))
    ng = {
        u"会社（四季報・予想・子会社・証券・投資会社以外）": len(re.findall(u"会社", re.sub(u"会社四季報|会社予想|子会社|証券会社|投資会社", u"", text))),
        u"割安・買い場・狙い目": len(re.findall(u"割安|買い場|狙い目|ねらい目|仕込み", text)),
        u"〜のです": len(re.findall(u"[^も]のです", text)),
        u"私": text.count(u"私"),
        u"感応度・キャッシュフロー・持分法・粗利益・信用スプレッド": len(re.findall(u"感応度|キャッシュフロー|持分法|粗利益|信用スプレッド|運転資本", text)),
        u"上がります・下がります": len(re.findall(u"上がります|下がります", text)),
    }
    hit = [u"%s %d件" % (k, v) for k, v in ng.items() if v]
    print(u"   禁止語チェック: %s" % (u" / ".join(hit) if hit else u"すべて0件"))


if __name__ == "__main__":
    main()
