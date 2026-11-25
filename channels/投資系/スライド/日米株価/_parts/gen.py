# -*- coding: utf-8 -*-
"""
スライドの型を関数にしたもの。各パート（pNN.py）は中身だけを書く。
マークアップは keizai-slide の reference-deck.html の各型をそのまま写している。
"""

def _hdr(sec):
    return u'  <div class="hdr"><span class="sec">%s</span><span class="brand"></span></div>\n' % sec


def _sec(cls, sec, inner):
    h = _hdr(sec) if sec is not None else u""
    return u'<section class="slide %s">\n%s%s</section>\n' % (cls, h, inner)


def _opt(tag, cls, val):
    return u'  <div class="%s">%s</div>\n' % (cls, val) if val else u""


def title(kicker, big, lead):
    return _sec("t-title", None, _opt("", "kicker", kicker) + _opt("", "big", big) + _opt("", "lead", lead))


def text(sec, lead, stmt, note=None):
    return _sec("t-text", sec, _opt("", "lead", lead) + _opt("", "stmt", stmt) + _opt("", "note", note))


def metric(sec, lbl, fig, unit=u"", sub=u"", lead=None, h=None, note=None, color="navy"):
    u = u'<span class="u">%s</span>' % unit if unit else u""
    m = (u'  <div class="metrics">\n    <div class="metric %s hero">\n      <div class="mlbl">%s</div>\n'
         u'      <div class="mfig">%s%s</div>\n      <div class="msub">%s</div>\n    </div>\n  </div>\n') % (color, lbl, fig, u, sub)
    return _sec("numviz t-metric", sec, _opt("", "lead", lead) + _opt("", "h-main", h) + m + _opt("", "note", note))


def metrics(sec, items, lead=None, h=None, note=None):
    """items: [(color, lbl, fig, unit, sub)] 2〜3個を横に"""
    longest = max(len(fig) + len(unit) for _, _, fig, unit, _ in items)
    out = u'  <div class="metrics two%s%s">\n' % (u" three" if len(items) == 3 else u"", u" long" if longest >= 9 else u"")
    for color, lbl, fig, unit, sub in items:
        u = u'<span class="u">%s</span>' % unit if unit else u""
        out += (u'    <div class="metric %s">\n      <div class="mlbl">%s</div>\n      <div class="mfig">%s%s</div>\n'
                u'      <div class="msub">%s</div>\n    </div>\n') % (color, lbl, fig, u, sub)
    out += u'  </div>\n'
    return _sec("numviz t-metric", sec, _opt("", "lead", lead) + _opt("", "h-main", h) + out + _opt("", "note", note))


def vs(sec, h, left, right, badge=None, mark=u"VS", foot=None, rcls="right", sub=None):
    """left/right: (name, cap, big, small)。small は left は small、right は strong で出す"""
    b = u'  <div class="badge navy">%s</div>\n' % badge if badge else u""
    def box(cls, t, strong):
        name, cap, big, small = t
        tail = (u'<div class="strong">%s</div>' if strong else u'<div class="small">%s</div>') % small if small else u""
        return (u'<div class="box %s"><div class="name">%s</div><div class="cap">%s</div><div class="big">%s</div>'
                u'<div class="div"></div>%s</div>') % (cls, name, cap, big, tail)
    inner = (b + _opt("", "h-main", h) + _opt("", "h-sub", sub) + u'  <div class="cols">\n    %s\n    <div class="vsmark">%s</div>\n    %s\n  </div>\n'
             % (box("left", left, False), mark, box(rcls, right, True)) + (u'  <div class="foot-note">%s</div>\n' % foot if foot else u""))
    return _sec("t-vs", sec, inner)


def cards(sec, h, items, sub=None, badge=None, foot=None, g2=False):
    """items: [(no, title, text)]"""
    b = u'  <div class="badge%s">%s</div>\n' % (u"" if badge and not badge.startswith("!") else u"", badge.lstrip("!")) if badge else u""
    out = u'  <div class="grid%s">\n' % (u" g2" if g2 else u"")
    for i, (no, t, tx) in enumerate(items, 1):
        out += u'    <div class="card c%d"><div class="cno">%s</div><div class="ctitle">%s</div><div class="ctext">%s</div></div>\n' % (i, no, t, tx)
    out += u'  </div>\n'
    fb = u'  <div class="foot-bar">%s</div>\n' % foot if foot else u""
    return _sec("t-cards", sec, b + _opt("", "h-main", h) + _opt("", "h-sub", sub) + out + fb)


def stats(sec, h, cols, sub=None, foot=None):
    """cols: [(nm, cd, lbl, val, tag, cls)]  cls は ''/'cblue'/'cnavy'"""
    out = u'  <div class="cols">\n'
    for nm, cd, lbl, val, tag, cls in cols:
        out += (u'    <div class="col %s"><div class="top"><div class="nm">%s</div><div class="cd">%s</div></div>'
                u'<div class="body"><div class="lbl">%s</div><div class="val2">%s</div><div class="tag">%s</div></div></div>\n') % (cls, nm, cd, lbl, val, tag)
    out += u'  </div>\n'
    fb = u'  <div class="foot-bar">%s</div>\n' % foot if foot else u""
    return _sec("t-stats", sec, _opt("", "h-main", h) + _opt("", "h-sub", sub) + out + fb)


def flow(sec, h, nodes, release=None, sep=u"→"):
    """nodes: [text] または [(text, kind)] kind: 'blue'/'orange'/'danger'"""
    styles = {"blue": u' style="border-bottom-color:var(--blue);color:var(--blue);"',
              "orange": u' style="border-bottom-color:var(--orange);color:#cf820f;"'}
    parts = []
    for n in nodes:
        t, k = (n, None) if isinstance(n, str) else n
        if k == "danger":
            parts.append(u'<div class="node danger">%s</div>' % t)
        else:
            parts.append(u'<div class="node"%s>%s</div>' % (styles.get(k, u""), t))
    chain = (u'\n    <div class="arr">%s</div>\n    ' % sep).join(parts)
    rel = u'  <div class="release">%s</div>\n' % release if release else u""
    ncls = u" n%d" % len(nodes) if len(nodes) >= 4 else u""
    return _sec("t-flow", sec, _opt("", "h-main", h) + u'  <div class="chain%s">\n    %s\n  </div>\n' % (ncls, chain) + rel)


def steps(sec, h, items, foot=None):
    """items: [(era, v)] 2〜3個"""
    parts = [u'<div class="step s%d"><div class="era">%s</div><div class="v">%s</div></div>' % (i, e, v) for i, (e, v) in enumerate(items, 1)]
    inner = _opt("", "h-main", h) + u'  <div class="steps">\n    %s\n  </div>\n' % u'\n    <div class="sarr">→</div>\n    '.join(parts)
    if foot:
        inner += u'  <div class="foot-note">%s</div>\n' % foot
    return _sec("t-steps", sec, inner)


def numline(sec, h, marks, foot=None):
    """marks: [(left%, val, lab, color or None)]"""
    out = u'  <div class="scale">\n'
    for left, val, lab, col in marks:
        st = u' style="color:%s"' % col if col else u""
        ds = u' style="background:%s"' % col if col else u""
        out += u'    <div class="mk" style="left:%s%%"><div class="val"%s>%s</div><div class="dot"%s></div><div class="lab">%s</div></div>\n' % (left, st, val, ds, lab)
    out += u'  </div>\n'
    fn = u'  <div class="foot-note">%s</div>\n' % foot if foot else u""
    return _sec("t-numline", sec, _opt("", "h-main", h) + out + fn)


def prop(sec, h, main, rest, lead=None, note=None):
    """main: (pct_text, label, width%)  rest: (pct_text, label)"""
    p, l, w = main
    out = (u'  <div class="pbar">\n    <div class="seg main" style="width:%s%%"><span class="p">%s</span><span class="l">%s</span></div>\n'
           u'    <div class="seg rest"><span class="p">%s</span><span class="l">%s</span></div>\n  </div>\n') % (w, p, l, rest[0], rest[1])
    return _sec("numviz t-prop", sec, _opt("", "lead", lead) + _opt("", "h-main", h) + out + _opt("", "note", note))


def stack(sec, h, segs, total, sub=None):
    """segs: [(name, val, width%)]"""
    out = u'  <div class="sbar">\n'
    for i, (n, v, w) in enumerate(segs):
        out += u'    <div class="seg %s" style="width:%s%%"><div class="sn">%s</div><div class="sv">%s</div></div>\n' % ("abc"[i % 3], w, n, v)
    out += u'  </div>\n'
    return _sec("t-stack", sec, _opt("", "h-main", h) + _opt("", "h-sub", sub) + out + u'  <div class="total">%s</div>\n' % total)


def vbars(sec, h, bars, sub=None, foot=None):
    """bars: [(height_px, val, cap, subcap, orange)]"""
    out = u'  <div class="vcols">\n'
    for hp, v, cap, sc, org in bars:
        out += u'    <div class="vb%s"><div class="bar" style="height:%dpx">%s</div><div class="cap">%s</div><div class="sub">%s</div></div>\n' % (u" orange" if org else u"", hp, v, cap, sc)
    out += u'  </div>\n'
    fb = u'  <div class="foot-bar">%s</div>\n' % foot if foot else u""
    return _sec("t-vbars", sec, _opt("", "h-main", h) + _opt("", "h-sub", sub) + out + fb)


def fx(sec, h, c1, c2, res, lead=None, note=None, a2=u"＝"):
    out = (u'  <div class="row">\n    <div class="card"><div class="c-l">%s</div><div class="c-v">%s</div></div>\n    <div class="arr">→</div>\n'
           u'    <div class="card"><div class="c-l">%s</div><div class="c-v">%s</div></div>\n    <div class="arr">%s</div>\n'
           u'    <div class="result"><div class="r-l">%s</div><div class="r-v">%s</div></div>\n  </div>\n') % (c1[0], c1[1], c2[0], c2[1], a2, res[0], res[1])
    return _sec("numviz t-fx", sec, _opt("", "lead", lead) + _opt("", "h-main", h) + out + _opt("", "note", note))


def rank(sec, h, rows, sub=None, compact=False):
    """rows: [(name, value, up)]"""
    out = u'  <div class="rows">\n'
    for n, v, up in rows:
        out += u'    <div class="row"><span class="nm">%s</span><span class="pct%s">%s</span></div>\n' % (n, u" up" if up else u"", v)
    out += u'  </div>\n'
    return _sec("t-rank" + (u" compact" if compact else u""), sec, _opt("", "h-main", h) + _opt("", "h-sub", sub) + out)


def agenda(sec, h, rows, cta=None, center=True):
    out = u'  <div class="rows">\n'
    for no, t, d in rows:
        out += u'    <div class="row"><span class="no">%s</span><span class="t">%s</span><span class="d">%s</span></div>\n' % (no, t, d)
    out += u'  </div>\n'
    c = u'  <div class="cta">%s</div>\n' % cta if cta else u""
    return _sec("t-agenda" + (u" center" if center else u""), sec, _opt("", "h-main", h) + out + c)


def port(sec, h, rows, foot=None, sub=None):
    """rows: [(label, width%, value_text, fillclass)] fillclass: f-cash/f-idx/f-jp/f-gold"""
    out = u'  <div class="bars">\n'
    for lab, w, val, f in rows:
        out += u'    <div class="brow"><span class="lab">%s</span><div class="track"><div class="fill %s" style="width:%s%%"></div><span class="pval">%s</span></div></div>\n' % (lab, f, w, val)
    out += u'  </div>\n'
    fb = u'  <div class="foot-bar">%s</div>\n' % foot if foot else u""
    return _sec("t-port", sec, _opt("", "h-main", h) + _opt("", "h-sub", sub) + out + fb)


def section(sec, part, total, num, ttl, desc, topic):
    inner = (u'  <div class="topic"><span>PART %d / %d</span><span class="bar"></span><span>%s</span></div>\n'
             u'  <div class="numbox">%02d</div>\n'
             u'  <div class="stitle"><div class="label">SECTION</div><div class="ttl">%s</div><div class="rule"></div><div class="desc">%s</div></div>\n') % (part, total, topic, num, ttl, desc)
    return _sec("t-section", sec, inner)


def board(sec, h, states, lead=None, note=None, labels=None, sub=None):
    """3条件ボード。states: 3つの (状態, 下の一言)。状態: 'q'=未点検 'ok'=立っていない 'hit'=立った 'now'=いま点検中"""
    labels = labels or [(u"条件1", u"供給"), (u"条件2", u"利益の<br>裏付け"), (u"条件3", u"信用")]
    out = u'  <div class="cond3">\n'
    for (n, t), (st, cap) in zip(labels, states):
        out += u'    <div class="cd %s"><span class="n">%s</span><span class="t">%s</span><span class="c">%s</span></div>\n' % (st, n, t, cap)
    out += u'  </div>\n'
    return _sec("t-cond", sec, _opt("", "lead", lead) + _opt("", "h-main", h) + _opt("", "h-sub", sub) + out + _opt("", "note", note))


def recovery(sec, h, rows, foot=None, sub=None):
    """戻るまでの時間の横棒。rows: [(label, months, text, long)]"""
    mx = 125.0
    out = []
    for lab, mo, txt, lng in rows:
        out.append((lab, max(round(mo / mx * 100, 1), 3), txt, u"f-jp" if lng else u"f-idx"))
    return port(sec, h, out, foot=foot, sub=sub)


def closing(big, sub):
    inner = (u'  <div class="big">%s</div>\n  <div class="sub">%s</div>\n'
             u'  <div class="tags"><span class="tg">👍 高評価</span><span class="tg">🔔 チャンネル登録</span><span class="tg">📣 ハイプ</span></div>\n') % (big, sub)
    return _sec("t-closing", None, inner)


def em(s):
    return u'<span class="em">%s</span>' % s
