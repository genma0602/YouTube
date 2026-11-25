# -*- coding: utf-8 -*-
import re, sys, io
from collections import Counter

p = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "koden"
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
    P("  %-26s %6d字 %5.1f%%  開始%5.1f%%  小見出し%d" % (b[0][:13], L, 100*L/N, 100*pos/N, len(b[2])))
    pos += L
longest = max(offs, key=lambda x: x[2])
P("  最長ブロック %s %.1f%%" % (longest[0][:12], 100*longest[2]/N))

sents = [s for s in re.split(r"[。！？]", body) if s.strip()]
over = sum(1 for pp in body_pars if len(pp) > 100)
P("[物理] 平均段落長 %.0f字 / 段落密度 %.0f/万字 / 平均文長 %.0f字 / 100字超 %d本(%.0f%%)" % (N/len(body_pars), len(body_pars)/man, N/len(sents), over, 100*over/len(body_pars)))

def positions(pat):
    return [100.0*m.start()/N for m in re.finditer(pat, body)]
def gaps(xs):
    g = []; prev = 0.0
    for x in xs: g.append(x-prev); prev = x
    g.append(100.0-prev); return max(g) if g else 100.0
sec = positions(r"あなた|持ち株|皆さん|ご自分|自分の株")
P("[二人称(旧定義)] %d箇所 %.1f/万字 最長空白 %.1fpt" % (len(sec), len(sec)/man, gaps(sec)))
P("  位置: " + " / ".join("%.0f" % x for x in sec))
sec2 = positions(r"あなた|持ち株|皆さん|ご自分|自分の株|お持ちの方|している方|された方|されている方|思われた方|思う方|思った方|思われるかもしれません|ください")
P("[二人称(拡張)] %d箇所 %.1f/万字 最長空白 %.1fpt" % (len(sec2), len(sec2)/man, gaps(sec2)))
pain = positions(r"気のせいではありません")
P("  痛みの承認: " + (", ".join("%.1f%%" % x for x in pain) if pain else "なし"))

hope_a = r"覇権|主役|欠かせない|追い風|強み|チャンス|本番"
fear = r"暴落|急落|崩壊|不安|下落|売られ|損|落ちる|落ち込|失望|リスク|下げ"
ha = len(re.findall(hope_a, body)); fe = len(re.findall(fear, body))
P("[感情] 希望語7語 %d回 %.1f/万字 / 恐れ語 %d回 %.1f/万字 / 比 %.2f" % (ha, ha/man, fe, fe/man, ha/max(fe,1)))
P("  希望語内訳: " + ", ".join("%s%d" % (k, v) for k, v in Counter(re.findall(hope_a, body)).most_common()))
hope_x = r"握って|欠かせな|必ず要|必要にな|強み|密集|先回り|チャンス|世界で初めて|世界シェア|世界で大きな|欠かせません"
P("  希望語(広義) %d回 %.1f/万字" % (len(re.findall(hope_x, body)), len(re.findall(hope_x, body))/man))

src = r"日本経済新聞|ブルームバーグ|ロイター|ブラックロック|ゴールドマン|JPモルガン|モルガン|四季報|東証|経済産業省|経産省|白書|によると|が調べたところ|と試算|報じ|公表|発表しました|説明しています|説明しました|と予測|と書いています"
sc = len(re.findall(src, body))
P("[出典] マーカー %d回 %.1f/万字  内訳: %s" % (sc, sc/man, ", ".join("%s%d" % (k, v) for k, v in Counter(re.findall(src, body)).most_common(8))))
act = len(re.findall(r"ください", body))
P("[行動指示] 「ください」%d回 %.1f/万字" % (act, act/man))
boku = len(re.findall(r"僕は|僕も|僕の|僕が", body))
P("[語り手] 僕は/も/の/が %d回 %.1f/万字" % (boku, boku/man))
P("[主語 /万字] " + " / ".join("%s %.1f" % (k, len(re.findall(pat, body))/man) for k, pat in [("日本", r"日本"), ("アメリカ", r"アメリカ|米国"), ("AI", r"AI"), ("金利", r"金利|国債"), ("日経", r"日経平均"), ("TOPIX", r"TOPIX"), ("中国", r"中国")]))

if mode == "koden":
    jp = r"DNP|大日本印刷|AGC|三菱電機|古河電工|住友電工|レゾナック|日産化学|デクセリアルズ|アドバンテスト|新光電気|フジクラ|キオクシア|NTT"
    us = r"NVIDIA|ブロードコム|TSMC|マイクロソフト|AWS|デル|Yole|Cignal"
else:
    jp = r"キオクシア|日本マクドナルド|マクドナルド|セリア|トライアル|ワークマン|ナカニシ|上村工業|精工技研|東映アニメーション|ヨネックス|沖縄セルラー|タイミー|freee|フェローテック|QDレーザ|パワーエックス|千代田化工|アストロスケール|Synspective|ティアフォー|三洋化成|新日本建設|ブロードリーフ|東芝|TDK|豊田通商|東レ|三菱電機|シンニホンコム|ユニオンサイト|トライサット|三菱UFJ|トヨタ"
    us = r"エヌビディア|マイクロソフト|グーグル|アマゾン|メタ|アップル|オープンAI|テスラ|ベインキャピタル|NVIDIA"
jc = len(re.findall(jp, body)); uc = len(re.findall(us, body))
P("[企業名] 日本 %d回 %.1f/万字 / 海外 %d回 %.1f/万字" % (jc, jc/man, uc, uc/man))
P("  ブロック別 日本/海外: " + " / ".join("%s %d/%d" % (b[0][:4], len(re.findall(jp, "".join(b[1]))), len(re.findall(us, "".join(b[1])))) for b in blocks))
jpos = positions(jp)
P("  社名の初出 %.1f%% / 社名の最長空白 %.1fpt / 10%%刻み: %s" % (jpos[0] if jpos else -1, gaps(jpos), " ".join(str(sum(1 for x in jpos if d <= x < d+10)) for d in range(0, 100, 10))))
# 数字つき銘柄の初出：社名の後ろ120字以内に%か倍か円か億
first_num = None
for m in re.finditer(jp, body):
    seg = body[m.end():m.end()+120]
    if re.search(r"[0-9][0-9,\.]*(%|倍|円|億)", seg):
        first_num = 100.0*m.start()/N; break
P("  数字つき銘柄の初出 %s" % ("%.1f%%" % first_num if first_num is not None else "なし"))

terms = list(re.finditer(r"とは、|というのは|と呼ばれます|と呼びます|正式には|思ってください|という言葉|のことです|という技術|の名前が|ということです", body))
land = sum(1 for m in terms if re.search(jp + r"|日経平均|TOPIX", body[m.end():m.end()+300]))
P("[説明の着地] 用語説明 %d箇所 %.1f/万字 / 300字以内に日本企業名 %.0f%%" % (len(terms), len(terms)/man, 100*land/max(len(terms),1)))

pp_ = len(re.findall(r"[0-9]+(?:\.[0-9]+)?%の上昇|約[0-9.]+倍|およそ[0-9.]+倍|[0-9.]+倍にな|[0-9.]+倍です", body))
mm_ = len(re.findall(r"[0-9]+(?:\.[0-9]+)?%の下落|[0-9]+(?:\.[0-9]+)?%下げ|[0-9]+割(?:下げ|安|減)|[0-9]+%(?:減|下回)|[0-9]+%安", body))
P("[名簿の符号] プラス %d件 / マイナス %d件" % (pp_, mm_))
P("[決まり文句] " + " / ".join("%s%d" % (k, len(re.findall(k, body))) for k in ["いちばん大事なところです", "さきほど", "正直にお伝えします", "気のせいではありません", "つまり", "ところが", "ただし", "だからこそ", "かもしれません"]))

# 理由パート（引数3：ブロック先頭文字の列。例 "⑥⑦⑤"）
if len(sys.argv) > 3:
    ids = sys.argv[3]
    rb = "".join("".join(b[1]) for b in blocks if b[0][:1] in ids)
    rm = len(rb)/10000.0
    P("[理由パート %s] %d字 / 日本 %.1f/万字 / 日本企業名 %.1f/万字 / 海外企業名 %.1f/万字" % (ids, len(rb), len(re.findall(r"日本", rb))/rm, len(re.findall(jp, rb))/rm, len(re.findall(us, rb))/rm))

io.open(sys.argv[4] if len(sys.argv) > 4 else "measure_out.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
