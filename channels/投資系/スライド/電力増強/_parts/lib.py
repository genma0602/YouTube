# -*- coding: utf-8 -*-
"""
電力増強・デッキの部品（gen.py から import する）

    gen.py から import して使う部品

書き方の約束：
  ・文字列の中の【…】は強調（<span class="em">）、\n は改行（<br>）
  ・本文は docs_電力増強/scenario_本文のみ.md の言い回しに合わせる
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_CSS = os.path.expanduser(r"~/.claude/skills/keizai-slide/assets/style.css")
TOTAL_SEC = 20

PARTS = []          # (name, sec_no, [html...])
CUR = {"n": 0, "label": "", "slides": None}


def esc(s):
    s = s.replace("&", "&amp;")
    s = re.sub(r"【(.*?)】", r'<span class="em">\1</span>', s, flags=re.S)
    return s.replace("\n", "<br>")


def part(name, n):
    CUR["n"] = n
    CUR["slides"] = []
    PARTS.append((name, n, CUR["slides"]))


def label(s):
    CUR["label"] = s


def hdr():
    return '<div class="hdr"><span class="sec">Section %d：%s</span><span class="brand"></span></div>' % (CUR["n"], esc(CUR["label"]))


def add(html, memo=""):
    CUR["slides"].append("<!-- %s -->\n%s" % (memo, html))


# ---------------- 型 ----------------
def title(kicker, big, lead):
    add('<section class="slide t-title">\n  <div class="kicker">%s</div>\n  <div class="big">%s</div>\n  <div class="lead">%s</div>\n</section>' % (esc(kicker), esc(big), esc(lead)), "タイトル")


def door(ttl, desc, topic):
    n = CUR["n"]
    add('<section class="slide t-section">\n  <div class="hdr"><span class="sec">Section %d：%s</span><span class="brand"></span></div>\n'
        '  <div class="topic"><span>PART %d / %d</span><span class="bar"></span><span>%s</span></div>\n'
        '  <div class="numbox">%d</div>\n'
        '  <div class="stitle"><div class="label">SECTION</div><div class="ttl">%s</div><div class="rule"></div><div class="desc">%s</div></div>\n</section>'
        % (n, esc(ttl.replace("\n", "")), n, TOTAL_SEC, esc(topic), n, esc(ttl), esc(desc)), "扉")


def text(lead, stmt, note=None):
    h = '<section class="slide t-text">\n  %s\n  <div class="lead">%s</div>\n  <div class="stmt">%s</div>\n' % (hdr(), esc(lead), esc(stmt))
    if note:
        h += '  <div class="note">%s</div>\n' % esc(note)
    add(h + '</section>', stmt[:12])


def vs(badge, h, L, R, note=None, mark="／"):
    """L/R = (name, cap, big)。L が青い箱（bluebox）"""
    s = '<section class="slide t-vs">\n  %s\n' % hdr()
    if badge:
        s += '  <div class="badge navy">%s</div>\n' % esc(badge)
    s += '  <div class="h-main">%s</div>\n  <div class="cols">\n' % esc(h)
    s += '    <div class="box bluebox"><div class="name">%s</div><div class="cap">%s</div><div class="big">%s</div></div>\n' % tuple(esc(x) for x in L)
    s += '    <div class="vsmark">%s</div>\n' % esc(mark)
    s += '    <div class="box left"><div class="name">%s</div><div class="cap">%s</div><div class="big">%s</div></div>\n  </div>\n' % tuple(esc(x) for x in R)
    if note:
        s += '  <div class="note" style="text-align:center;font-size:22px;color:#7a828c;margin-top:18px;">%s</div>\n' % esc(note)
    add(s + '</section>', h[:12])


def cards(h, sub, items, cols=None):
    """items = [(title, text)]"""
    n = len(items)
    if cols is None:
        cols = n
    cls = {2: "grid g2", 3: "grid", 4: "grid g4", 5: "grid g5", 6: "grid g5"}[cols]
    style = ' style="grid-template-columns:repeat(%d,1fr);gap:16px"' % cols if cols >= 4 else ""
    s = '<section class="slide t-cards">\n  %s\n  <div class="h-main">%s</div>\n' % (hdr(), esc(h))
    if sub:
        s += '  <div class="h-sub">%s</div>\n' % esc(sub)
    s += '  <div class="%s"%s>\n' % (cls, style)
    for i, (t, x) in enumerate(items):
        s += '    <div class="card c%d"><div class="cno">%d</div><div class="ctitle">%s</div>%s</div>\n' % (
            i % 4 + 1, i + 1, esc(t), ('<div class="ctext">%s</div>' % esc(x)) if x else "")
    add(s + '  </div>\n</section>', h[:12])


def stats(h, sub, cols):
    """cols = [(nm, cd, lbl, val, color)] color: cnavy/cblue/''"""
    s = '<section class="slide t-stats">\n  %s\n  <div class="h-main">%s</div>\n' % (hdr(), esc(h))
    if sub:
        s += '  <div class="h-sub">%s</div>\n' % esc(sub)
    s += '  <div class="cols">\n'
    for nm, cd, lb, val, color in cols:
        s += '    <div class="col %s"><div class="top"><div class="nm">%s</div><div class="cd">%s</div></div><div class="body"><div class="lbl">%s</div><div class="val2">%s</div></div></div>\n' % (
            color, esc(nm), esc(cd), esc(lb), esc(val))
    add(s + '  </div>\n</section>', h[:12])


def metric(lead, lbl, fig, unit="", sub="", color="navy", fs=None):
    st = ' style="font-size:%dpx"' % fs if fs else ""
    u = '<span class="u">%s</span>' % esc(unit) if unit else ""
    add('<section class="slide numviz t-metric">\n  %s\n  <div class="lead">%s</div>\n  <div class="metrics">\n'
        '    <div class="metric %s hero">\n      <div class="mlbl">%s</div>\n      <div class="mfig"%s>%s%s</div>\n      <div class="msub">%s</div>\n    </div>\n  </div>\n</section>'
        % (hdr(), esc(lead), color, esc(lbl), st, esc(fig), u, esc(sub)), lbl[:12])


def flow(h, nodes, release=None, danger=(), blue=(), arrows=None):
    s = '<section class="slide t-flow">\n  %s\n  <div class="h-main">%s</div>\n  <div class="chain">\n' % (hdr(), esc(h))
    for i, nd in enumerate(nodes):
        if i:
            s += '    <div class="arr">%s</div>\n' % (arrows[i - 1] if arrows else "→")
        if i in danger:
            s += '    <div class="node danger">%s</div>\n' % esc(nd)
        elif i in blue:
            s += '    <div class="node" style="border-bottom-color:var(--blue);color:var(--blue);">%s</div>\n' % esc(nd)
        else:
            s += '    <div class="node">%s</div>\n' % esc(nd)
    s += '  </div>\n'
    if release:
        s += '  <div class="release">%s</div>\n' % esc(release)
    add(s + '</section>', h[:12])


def fx(h, a, b, r, mid="→", end="＝"):
    """a/b = (label, value)、r = (label, value)"""
    add('<section class="slide numviz t-fx">\n  %s\n  <div class="h-main">%s</div>\n  <div class="row">\n'
        '    <div class="card"><div class="c-l">%s</div><div class="c-v">%s</div></div>\n    <div class="arr">%s</div>\n'
        '    <div class="card"><div class="c-l">%s</div><div class="c-v">%s</div></div>\n    <div class="arr">%s</div>\n'
        '    <div class="result"><div class="r-l">%s</div><div class="r-v">%s</div></div>\n  </div>\n</section>'
        % (hdr(), esc(h), esc(a[0]), esc(a[1]), mid, esc(b[0]), esc(b[1]), end, esc(r[0]), esc(r[1])), h[:12])


def prop(lead, h, pct, p, l, rp, rl):
    add('<section class="slide numviz t-prop">\n  %s\n  <div class="lead">%s</div>\n  <div class="h-main">%s</div>\n  <div class="pbar">\n'
        '    <div class="seg main" style="width:%d%%"><span class="p">%s</span><span class="l">%s</span></div>\n'
        '    <div class="seg rest"><span class="p">%s</span><span class="l">%s</span></div>\n  </div>\n</section>'
        % (hdr(), esc(lead), esc(h), pct, esc(p), esc(l), esc(rp), esc(rl)), h[:12])


def agenda(h, rows, cta=None):
    s = '<section class="slide t-agenda center">\n  %s\n  <div class="h-main">%s</div>\n  <div class="rows">\n' % (hdr(), esc(h))
    for i, (t, d) in enumerate(rows, 1):
        s += '    <div class="row"><span class="no">%d</span><span class="t">%s</span><span class="d">%s</span></div>\n' % (i, esc(t), esc(d))
    s += '  </div>\n'
    if cta:
        s += '  <div class="cta">%s</div>\n' % esc(cta)
    add(s + '</section>', h[:12])


def image(fn, alt):
    add('<section class="slide t-image"><img src="img/%s.png" alt="%s"></section>' % (fn, alt), "画像：" + fn)


RULES = [("1", "誰に借りているか"), ("2", "何の通貨で\n借りているか"), ("3", "どれだけ速く\n直せるか")]


def rulemap(h, on=(), subs=None, cn=None, cc=None, note=None, done=()):
    """subs = {0: (text, 'ng'|'ok'|'')}"""
    s = '<section class="slide t-map">\n  %s\n  <div class="h-main">%s</div>\n  <div class="flowmap">\n' % (hdr(), esc(h))
    for i, (no, t) in enumerate(RULES):
        cls = "fm on" if i in on else ("fm done" if i in done else "fm")
        sub = ""
        if subs and i in subs:
            tx, kind = subs[i]
            sub = '<span class="s %s">%s</span>' % (kind, esc(tx))
        s += '    <div class="%s"><span class="n">%s</span>%s%s</div>\n' % (cls, no, esc(t), sub)
    s += '  </div>\n'
    if cn:
        s += '  <div class="coname"><div class="cn">%s</div>%s</div>\n' % (esc(cn), ('<div class="cc">%s</div>' % esc(cc)) if cc else "")
    if note:
        s += '  <div class="note">%s</div>\n' % esc(note)
    add(s + '</section>', "帯：" + h[:10])


def vbars(h, sub, bars, foot=None):
    """bars = [(value_label, height_px, cap, sub, orange)] 高さは値に比例させて呼ぶ側で決める（最大300px）"""
    s = '<section class="slide t-vbars">\n  %s\n  <div class="h-main">%s</div>\n' % (hdr(), esc(h))
    if sub:
        s += '  <div class="h-sub">%s</div>\n' % esc(sub)
    s += '  <div class="vcols%s">\n' % (" wide" if len(bars) <= 3 else "")
    for v, ht, cap, sb, org in bars:
        s += '    <div class="vb%s"><div class="bar" style="height:%dpx">%s</div><div class="cap">%s</div><div class="sub">%s</div></div>\n' % (
            " orange" if org else "", max(int(ht * 0.8), 64), esc(v), esc(cap), esc(sb))
    s += '  </div>\n'
    if foot:
        s += '  <div class="foot-bar">%s</div>\n' % esc(foot)
    add(s + '</section>', h[:12])


def steps(h, items):
    """items = [(era, v)] 2〜3段。最後がオレンジ"""
    cls = ["s1", "s2", "s3"][-len(items):] if len(items) <= 3 else ["s1"] * (len(items) - 2) + ["s2", "s3"]
    s = '<section class="slide t-steps">\n  %s\n  <div class="h-main">%s</div>\n  <div class="steps">\n' % (hdr(), esc(h))
    for i, (era, v) in enumerate(items):
        if i:
            s += '    <div class="sarr">→</div>\n'
        s += '    <div class="step %s"><div class="era">%s</div><div class="v">%s</div></div>\n' % (cls[i], esc(era), esc(v))
    add(s + '  </div>\n</section>', h[:12])


def stack(h, sub, segs, total):
    """segs = [(name, value, width_pct)] a/b/c の色"""
    s = '<section class="slide t-stack">\n  %s\n  <div class="h-main">%s</div>\n' % (hdr(), esc(h))
    if sub:
        s += '  <div class="h-sub">%s</div>\n' % esc(sub)
    s += '  <div class="sbar">\n'
    for i, (nm, v, w) in enumerate(segs):
        s += '    <div class="seg %s" style="width:%s%%"><div class="sn">%s</div><div class="sv">%s</div></div>\n' % ("abc"[i % 3], w, esc(nm), esc(v))
    s += '  </div>\n  <div class="total">%s</div>\n' % esc(total)
    add(s + '</section>', h[:12])


def closing(big, sub, tags=True):
    t = '\n  <div class="tags"><span class="tg">👍 高評価</span><span class="tg">🔔 チャンネル登録</span><span class="tg">⚡ ハイプボタン</span></div>' if tags else ""
    add('<section class="slide t-closing">\n  <div class="big">%s</div>\n  <div class="sub">%s</div>%s\n</section>' % (esc(big), esc(sub), t), "締め")


# =====================================================================
