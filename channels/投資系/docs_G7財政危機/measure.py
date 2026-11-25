# -*- coding: utf-8 -*-
"""G7財政危機 台本の型の数値を測る。docs_光電融合/measure.py を元に、この企画の社名・機関名に合わせた。
使い方: python -I docs_G7財政危機/measure.py docs_G7財政危機/scenario_draft.md [出力先]
"""
import re, sys, io
from collections import Counter

p = sys.argv[1]
raw = io.open(p, encoding="utf-8").read().split("\n")

blocks = []
cur = None
for ln in raw:
    if ln.startswith("## "):
        cur = [ln[3:].strip(), [], []]
        blocks.append(cur); continue
    if cur is None: continue
    if ln.startswith("### "):
        cur[2].append(ln[4:].strip()); continue
    if ln.startswith(">") or ln.startswith("#") or ln.startswith("---") or ln.startswith("|") or ln.strip() == "":
        continue
    cur[1].append(ln.strip())

body_pars = [pp for b in blocks for pp in b[1]]
body = "".join(body_pars)
N = len(body); man = N / 10000.0
out = []
def P(s): out.append(s)

P("本文字数 %d  段落 %d  ブロック %d  小見出し %d" % (N, len(body_pars), len(blocks), sum(len(b[2]) for b in blocks)))
P("[ブロック配分]")
offs = []; pos = 0
for b in blocks:
    L = sum(len(pp) for pp in b[1]); offs.append((b[0], pos, L))
    longest_par = max((len(pp) for pp in b[1]), default=0)
    P("  %-28s %6d字 %5.1f%%  開始%5.1f%%  小見出し%d  最長段落%d字" % (b[0][:14], L, 100*L/N, 100*pos/N, len(b[2]), longest_par))
    pos += L
longest = max(offs, key=lambda x: x[2])
P("  最長ブロック %s %.1f%%" % (longest[0][:12], 100*longest[2]/N))

# 役割別の尺
def share(ids):
    return 100.0 * sum(sum(len(pp) for pp in b[1]) for b in blocks if b[0][:1] in ids) / N
P("[尺] 中和① %.1f%% / 理由②③⑤⑥⑦⑧⑨⑩ %.1f%% / 処方箋・再定義④⑪⑫⑬⑭⑮ %.1f%% / 締め⑯ %.1f%%" % (share("①"), share("②③⑤⑥⑦⑧⑨⑩"), share("④⑪⑫⑬⑭⑮"), share("⑯")))

sents = [s for s in re.split(r"[。！？]", body) if s.strip()]
over = sum(1 for pp in body_pars if len(pp) > 100)
over150 = [pp for pp in body_pars if len(pp) > 150]
P("[物理] 平均段落長 %.0f字 / 段落密度 %.0f/万字 / 平均文長 %.0f字 / 100字超 %d本(%.0f%%) / 150字超 %d本 / 最長 %d字" % (N/len(body_pars), len(body_pars)/man, N/len(sents), over, 100*over/len(body_pars), len(over150), max(len(pp) for pp in body_pars)))
for pp in sorted(over150, key=len, reverse=True)[:5]:
    P("    %d字: %s…" % (len(pp), pp[:40]))

neg = sum(1 for s in sents if re.search(r"(ません|ない|ませんでした|なかった|ありません)$", s.strip()))
P("[否定で終わる文] %d/%d = %.1f%%" % (neg, len(sents), 100*neg/len(sents)))

def positions(pat):
    return [100.0*m.start()/N for m in re.finditer(pat, body)]
def gaps(xs):
    g = []; prev = 0.0
    for x in xs: g.append(x-prev); prev = x
    g.append(100.0-prev)
    if not g: return (100.0, 0, 100)
    i = max(range(len(g)), key=lambda k: g[k])
    lo = xs[i-1] if i > 0 else 0.0
    hi = xs[i] if i < len(xs) else 100.0
    return (g[i], lo, hi)

sec = positions(r"あなた|持ち株|皆さん|ご自分|自分の株")
g = gaps(sec)
P("[二人称(旧定義)] %d箇所 %.1f/万字 最長空白 %.1fpt（%.1f→%.1f%%）" % (len(sec), len(sec)/man, g[0], g[1], g[2]))
sec2 = positions(r"あなた|持ち株|皆さん|ご自分|自分の株|お持ちの方|している方|された方|されている方|思われた方|思う方|思った方|思われるかもしれません|ください|持っている方|買う方|積み立ての方|積み立てだけの方|聞いてきた方|思っていた方|安心した方|多い方")
g2 = gaps(sec2)
P("[二人称(拡張)] %d箇所 %.1f/万字 最長空白 %.1fpt（%.1f→%.1f%%）" % (len(sec2), len(sec2)/man, g2[0], g2[1], g2[2]))
P("  位置: " + " / ".join("%.0f" % x for x in sec2))
pain = positions(r"気のせいではありません|不安になるのは当然|当然です")
P("  痛みの承認: " + (", ".join("%.1f%%" % x for x in pain) if pain else "なし"))

hope_a = r"覇権|主役|欠かせない|追い風|強み|チャンス|本番"
hope_b = r"覇権|主役|欠かせない|欠かせません|追い風|強み|チャンス|本番|出番|取り合い|余地|厚い|伸びて|増えて|増え続け|戻ってき|買い集め|過去最高"
fear = r"暴落|急落|崩壊|不安|下落|売られ|損|落ちる|落ち込|失望|リスク|下げ"
fear_t = fear + r"|破綻|危ない|暴動|逃げ"
ha = len(re.findall(hope_a, body)); hb = len(re.findall(hope_b, body)); fe = len(re.findall(fear, body)); ft = len(re.findall(fear_t, body))
P("[感情] 希望語7語 %d回 %.1f/万字 / 希望語(拡張) %d回 %.1f/万字 / 恐れ語(標準) %d回 %.1f/万字 / 恐れ語(＋破綻・危ない・暴動・逃げ) %d回 %.1f/万字" % (ha, ha/man, hb, hb/man, fe, fe/man, ft, ft/man))
P("  比 7語/標準 %.2f / 拡張/標準 %.2f / 拡張/テーマ込み %.2f" % (ha/max(fe,1), hb/max(fe,1), hb/max(ft,1)))
P("  希望語(拡張)内訳: " + ", ".join("%s%d" % (k, v) for k, v in Counter(re.findall(hope_b, body)).most_common()))
P("  恐れ語(テーマ込み)内訳: " + ", ".join("%s%d" % (k, v) for k, v in Counter(re.findall(fear_t, body)).most_common()))
P("  ブロック別 希望(拡張)/恐れ(テーマ込み): " + " / ".join("%s %d/%d" % (b[0][:1], len(re.findall(hope_b, "".join(b[1]))), len(re.findall(fear_t, "".join(b[1])))) for b in blocks))

src = r"日本経済新聞|ブルームバーグ|ロイター|ブラックロック|ゴールドマン|JPモルガン|モルガン|四季報|東証|経済産業省|経産省|白書|によると|が調べたところ|と試算|報じ|公表|発表しました|説明しています|説明しました|と予測|と書いています"
src2 = src + r"|財務省|IMF|日銀|ECB|FRB|連銀|イングランド銀行|ステート・ストリート|オービス|シティ|会社予想|決算|分析しています|報告書|資料|統計|試算|書いてあります|認めました|明文化"
sc = len(re.findall(src, body)); sc2 = len(re.findall(src2, body))
P("[出典] 標準マーカー %d回 %.1f/万字 / 拡張 %d回 %.1f/万字  内訳: %s" % (sc, sc/man, sc2, sc2/man, ", ".join("%s%d" % (k, v) for k, v in Counter(re.findall(src2, body)).most_common(12))))
act = positions(r"ください")
ga = gaps(act)
P("[行動指示] 「ください」%d回 %.1f/万字 最長空白 %.1fpt（%.1f→%.1f%%）" % (len(act), len(act)/man, ga[0], ga[1], ga[2]))
boku = len(re.findall(r"僕は|僕も|僕の|僕が", body))
P("[語り手] 僕は/も/の/が %d回 %.1f/万字" % (boku, boku/man))
P("[主語 /万字] " + " / ".join("%s %.1f" % (k, len(re.findall(pat, body))/man) for k, pat in [("日本", r"日本"), ("アメリカ", r"アメリカ|米国"), ("フランス", r"フランス"), ("金利", r"金利"), ("国債", r"国債"), ("借金", r"借金"), ("破綻", r"破綻"), ("安全への支出", r"安全への支出"), ("買い手", r"買い手")]))

jp = r"ALSOK|キヤノン|セキュア|セコム|セーフィー|明治安田|日本ドライケミカル|TOUCH TO GO|テスコムジャパン|日東通信"
us = r"オービス|モルガン・スタンレー|シティグループ|ステート・ストリート|Axis|Milestone|BriefCam|パロアルト|リコー"
jc = len(re.findall(jp, body)); uc = len(re.findall(us, body))
P("[企業名] 日本 %d回 %.1f/万字 / 海外 %d回 %.1f/万字" % (jc, jc/man, uc, uc/man))
P("  ブロック別 日本/海外: " + " / ".join("%s %d/%d" % (b[0][:1], len(re.findall(jp, "".join(b[1]))), len(re.findall(us, "".join(b[1])))) for b in blocks))
jpos = positions(jp)
gj = gaps(jpos)
P("  社名の初出 %.1f%% / 社名の最長空白 %.1fpt（%.1f→%.1f%%） / 10%%刻み: %s" % (jpos[0] if jpos else -1, gj[0], gj[1], gj[2], " ".join(str(sum(1 for x in jpos if d <= x < d+10)) for d in range(0, 100, 10))))
first_num = None
for m in re.finditer(jp, body):
    seg = body[m.end():m.end()+120]
    if re.search(r"[0-9][0-9,\.]*(%|倍|円|億)", seg):
        first_num = 100.0*m.start()/N; break
P("  数字つき銘柄の初出 %s" % ("%.1f%%" % first_num if first_num is not None else "なし"))
for b in blocks:
    if b[0].startswith("④"):
        P("  1社フル（④）の開始 %.1f%%" % (100.0*offs[blocks.index(b)][1]/N))

terms = list(re.finditer(r"とは、|というのは|と呼ばれます|と呼びます|正式には|思ってください|という言葉|のことです|という技術|の名前が|ということです|といって、", body))
land = sum(1 for m in terms if re.search(jp, body[m.end():m.end()+300]))
P("[説明の着地] 用語説明 %d箇所 %.1f/万字 / 300字以内に日本企業名 %.0f%%" % (len(terms), len(terms)/man, 100*land/max(len(terms),1)))

nisa = positions(r"NISA|ETF|積み立て|オルカン|S&P500|成長投資枠")
P("[NISA・ETF] %d回 %.1f/万字  初出 %.1f%%  位置: %s" % (len(nisa), len(nisa)/man, nisa[0] if nisa else -1, " ".join("%.0f" % x for x in nisa[:40])))

yokoku = r"3社目で見ます|2社目です|最後にもう一度|後回しにした|伏せた話|答えます|その答えの前に|その1社目を|最後に、冒頭で|ここで開きます|最後にもう一度出てきます|見ていきます|あとで|このあと"
yk = list(re.finditer(yokoku, body))
P("[予告] %d回 %.1f/万字  内訳: %s" % (len(yk), len(yk)/man, ", ".join("%s@%.0f%%" % (m.group(0), 100.0*m.start()/N) for m in yk)))

P("[決まり文句] " + " / ".join("%s%d" % (k, len(re.findall(k, body))) for k in ["いちばん大事なところです", "さきほど", "正直に", "気のせいではありません", "つまり", "ところが", "ただし", "だからこそ", "かもしれません", "では、", "ここで、", "ここで", "思います", "はずです", "当然", "と思ってください", "いま", "次は、", "破綻する側ではありません", "危ない側", "3つのルール", "誰に借りているか", "何の通貨で借りているか", "どれだけ速く直せるか", "安全への支出", "買い手", "逆を向いて", "見てください"]))

# 理由パート
rb = "".join("".join(b[1]) for b in blocks if b[0][:1] in "②③⑤⑥⑦⑧⑨⑩")
rm = len(rb)/10000.0
P("[理由パート ②③⑤⑥⑦⑧⑨⑩] %d字 / 日本 %.1f/万字 / 日本企業名 %.1f/万字 / 海外企業名 %.1f/万字 / 二人称(拡張) %.1f/万字" % (len(rb), len(re.findall(r"日本", rb))/rm, len(re.findall(jp, rb))/rm, len(re.findall(us, rb))/rm, len(re.findall(r"あなた|持ち株|皆さん|ご自分|自分の株|お持ちの方|している方|された方|されている方|思われた方|思う方|思った方|ください|持っている方|聞いてきた方|思っていた方|安心した方", rb))/rm))

io.open(sys.argv[2] if len(sys.argv) > 2 else "measure_out.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
