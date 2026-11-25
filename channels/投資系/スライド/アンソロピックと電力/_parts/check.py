# -*- coding: utf-8 -*-
"""
レイアウトの機械点検（目視だけだと漏れるので）

    python check.py

・t-fx   … カード＋矢印＋結果の合計幅が 1200px を超えていないか
・t-flow … ノード＋矢印の合計幅が 1168px を超えていないか
・t-vs   … .big が 414px（箱の内寸）を超えて折り返していないか
・t-stage… 6枠の文字が 177px を超えていないか
・t-agenda … 行数が3を超えていないか
・t-steps … .v が 264px（step内寸）を超えていないか
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", u"アンソロピックと電力.html")
doc = io.open(HTML, encoding="utf-8").read()

HALF = set(u"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,:;%+-/()[]!?'\"&")


def w(text, fs):
    """文字幅の見積り（半角0.5em・全角1.0em、palt で全角は0.96）"""
    t = 0.0
    for ch in text:
        t += 0.5 if ch in HALF else 0.96
    return t * fs


def strip(s):
    s = re.sub(r"<br\s*/?>", u"\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.replace(u"&amp;", u"&").strip()


def lines(s):
    return [l for l in strip(s).split(u"\n") if l]


def inline_fs(tag, default):
    m = re.search(r'font-size:(\d+)px', tag)
    return int(m.group(1)) if m else default


slides = re.findall(r'<section class="slide ([^"]+)">(.*?)</section>', doc, re.S)
print(u"スライド %d 枚を点検" % len(slides))
bad = []

for i, (cls, body) in enumerate(slides, 1):
    c = cls.split()
    # ---- t-fx ----
    if "t-fx" in c:
        total = 0.0
        for tag, inner in re.findall(r'<div class="card"[^>]*>(.*?)</div>\s*</div>|()', body, re.S):
            pass
        for m in re.finditer(r'<div class="card">(.*?)</div></div>', body, re.S):
            seg = m.group(1)
            cl = re.search(r'<div class="c-l">(.*?)</div>', seg, re.S)
            cv = re.search(r'<div class="c-v"([^>]*)>(.*?)$', seg, re.S)
            wl = w(strip(cl.group(1)), 21) if cl else 0
            wv = w(strip(cv.group(2)), inline_fs(cv.group(1), 48)) if cv else 0
            total += max(wl, wv) + 60
        for m in re.finditer(r'<div class="result">(.*?)</div></div>', body, re.S):
            seg = m.group(1)
            rl = re.search(r'<div class="r-l">(.*?)</div>', seg, re.S)
            rv = re.search(r'<div class="r-v"([^>]*)>(.*?)$', seg, re.S)
            wl = w(strip(rl.group(1)), 21) if rl else 0
            wv = w(strip(rv.group(2)), inline_fs(rv.group(1), 58)) if rv else 0
            total += max(wl, wv) + 76
        narr = len(re.findall(r'<div class="arr">', body))
        total += narr * 76
        if total > 1200:
            bad.append((i, "t-fx", u"合計 %dpx（上限1200）" % total))
    # ---- t-flow ----
    if "t-flow" in c:
        total = 0.0
        for m in re.finditer(r'<div class="node[^"]*"[^>]*>(.*?)</div>', body, re.S):
            nw = max([w(l, 27) for l in lines(m.group(1))] or [0])
            total += max(nw + 56, 200)
        total += len(re.findall(r'<div class="arr">', body)) * 76
        if total > 1168:
            bad.append((i, "t-flow", u"合計 %dpx（上限1168）" % total))
    # ---- t-vs ----
    if "t-vs" in c:
        for m in re.finditer(r'<div class="big"[^>]*>(.*?)</div>', body, re.S):
            bw = max([w(l, 46) for l in lines(m.group(1))] or [0])
            if bw > 414:
                bad.append((i, "t-vs .big", u"%dpx（内寸414）「%s」" % (bw, strip(m.group(1)))))
        for m in re.finditer(r'<div class="name">(.*?)</div>', body, re.S):
            bw = w(strip(m.group(1)), 32)
            if bw > 414:
                bad.append((i, "t-vs .name", u"%dpx「%s」" % (bw, strip(m.group(1)))))
    # ---- t-stage ----
    if "t-stage" in c:
        mapmode = 'stagemap map' in body
        fs = 25 if mapmode else 30
        for m in re.finditer(r'<div class="st[^"]*">(.*?)</div>', body, re.S):
            seg = re.sub(r'<span class="n">.*?</span>', '', m.group(1), flags=re.S)
            seg = re.sub(r'<span class="co[^"]*">.*?</span>', '', seg, flags=re.S)
            sw = w(strip(seg), fs)
            if sw > 177:
                bad.append((i, "stagemap", u"%dpx（枠177）「%s」" % (sw, strip(seg))))
    # ---- t-agenda ----
    if "t-agenda" in c:
        n = len(re.findall(r'<div class="row">', body))
        if n > 3:
            bad.append((i, "t-agenda", u"%d行（上限3）" % n))
    # ---- t-steps ----
    if "t-steps" in c:
        for m in re.finditer(r'<div class="v"([^>]*)>(.*?)</div>', body, re.S):
            vw = max([w(l, inline_fs(m.group(1), 50)) for l in lines(m.group(2))] or [0])
            if vw > 264:
                bad.append((i, "t-steps .v", u"%dpx（内寸264）「%s」" % (vw, strip(m.group(2)))))
    # ---- t-text の大きい文（54px・内寸1080px。行末に1〜2字だけ残るのを防ぐ） ----
    if "t-text" in c:
        for m in re.finditer(r'<div class="stmt"[^>]*>(.*?)</div>', body, re.S):
            for l in lines(m.group(1)):
                lw = w(l, 54)
                if lw > 1080:
                    bad.append((i, "t-text .stmt", u"%dpx（内寸1080）「%s」" % (lw, l)))
    # ---- t-metric（社名の大きい字） ----
    if "t-metric" in c:
        for m in re.finditer(r'<div class="mfig"([^>]*)>(.*?)</div>', body, re.S):
            fs = inline_fs(m.group(1), 150)
            seg = m.group(2)
            u_m = re.search(r'<span class="u"([^>]*)>(.*?)</span>', seg, re.S)
            main = w(strip(re.sub(r'<span class="u".*?</span>', '', seg, flags=re.S)), fs)
            sub = w(strip(u_m.group(2)), inline_fs(u_m.group(1), int(fs * 0.45))) if u_m else 0
            if main + sub > 880:
                bad.append((i, "t-metric .mfig", u"%dpx（箱の内寸およそ880）" % (main + sub)))

if bad:
    print(u"\n★ 要確認 %d件" % len(bad))
    for i, k, msg in bad:
        print(u"  slide_%03d  %-14s %s" % (i, k, msg))
else:
    print(u"\nはみ出しの見積りに引っかかるものはありません")
