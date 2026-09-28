import re, sys
p = sys.argv[1]
raw = open(p, encoding="utf-8").read().split("\n")

# ---- 本文（注記・見出し・区切り・表を除外）とブロック分割
blocks = []   # (title, [paragraph lines])
cur = None
for ln in raw:
    if ln.startswith("## "):
        cur = [ln[3:].strip(), [], []]  # title, paragraphs, subheads
        blocks.append(cur)
        continue
    if cur is None:
        continue
    if ln.startswith("### "):
        cur[2].append(ln[4:].strip()); continue
    if ln.startswith(">") or ln.startswith("#") or ln.startswith("---") or ln.startswith("|"):
        continue
    if ln.strip() == "":
        continue
    cur[1].append(ln.strip())

body_pars = [pp for b in blocks for pp in b[1]]
body = "".join(body_pars)
N = len(body)
man = N / 10000.0
print(f"本文字数: {N}（{man:.2f}万字）  段落数: {len(body_pars)}  ブロック数: {len(blocks)}  小見出し数: {sum(len(b[2]) for b in blocks)}")

# ---- ブロック配分
print("\n[ブロック配分]")
offs = []
pos = 0
for b in blocks:
    L = sum(len(pp) for pp in b[1])
    offs.append((b[0], pos, L))
    print(f"  {b[0][:22]:<24} {L:>6}字  {100*L/N:5.1f}%  小見出し{len(b[2])}")
    pos += L
longest = max(offs, key=lambda x: x[2])
print(f"  最長ブロック: {longest[0][:20]} {100*longest[2]/N:.1f}%")

# ---- 段落・文
sents = [s for s in re.split(r"[。！？]", body) if s.strip()]
print(f"\n[読み上げの物理] 平均段落長 {N/len(body_pars):.0f}字 / 段落密度 {len(body_pars)/man:.0f}/万字 / 平均文長 {N/len(sents):.0f}字 / 100字超の段落 {sum(1 for pp in body_pars if len(pp)>100)}本（{100*sum(1 for pp in body_pars if len(pp)>100)/len(body_pars):.0f}%） / 150字超 {sum(1 for pp in body_pars if len(pp)>150)}本")

# ---- 二人称の位置
def positions(pattern):
    return [100.0*m.start()/N for m in re.finditer(pattern, body)]
sec = positions(r"あなた|持ち株|皆さん|ご自分|自分の株")
gaps = []
prev = 0.0
for x in sec:
    gaps.append(x-prev); prev = x
gaps.append(100.0-prev)
print(f"\n[視聴者の存在] 呼びかけ {len(sec)}箇所 / {len(sec)/man:.1f}回/万字 / 最長空白 {max(gaps):.1f}pt")
print("  出現位置(%): " + " / ".join(f"{x:.1f}" for x in sec))
pain = positions(r"気のせいではありません")
print(f"  痛みの承認「気のせいではありません」位置: " + (", ".join(f"{x:.1f}%" for x in pain) if pain else "なし"))

# ---- 希望語・恐れ語
hope_a = r"覇権|主役|欠かせない|追い風|強み|チャンス|本番"
hope_b = r"主役|広がる|広がって|初めて|道が開|選ばれ|追い風|強み|欠かせない|本番"
fear = r"暴落|急落|崩壊|不安|下落|売られ|損|落ちる|落ち込|失望|リスク|下げ"
ha = len(re.findall(hope_a, body)); hb = len(re.findall(hope_b, body)); fe = len(re.findall(fear, body))
print(f"\n[感情] 希望語(分析の7語) {ha}回 {ha/man:.1f}/万字 / 希望語(HANDOFF基準) {hb}回 {hb/man:.1f}/万字 / 恐れ語(近似) {fe}回 {fe/man:.1f}/万字 / 比 {ha/max(fe,1):.2f}")
from collections import Counter
print("  希望語の内訳: " + ", ".join(f"{k}{v}" for k,v in Counter(re.findall(hope_b, body)).most_common()))

# ---- 出典・行動指示・一人称
src = r"日本経済新聞|ブルームバーグ|マネックス証券|ブラックロック|大和総研|岡三証券|ダイヤモンド・ザイ|マン・グループ|ゴールドマン・サックス|UBS|リサーチ・アフィリエイツ|SMBC日興証券|大和証券|会社四季報|四季報|東証|によると|が調べたところ|と試算|報じ"
sc = len(re.findall(src, body))
named = Counter(re.findall(r"日本経済新聞|ブルームバーグ|マネックス証券|ブラックロック|大和総研|岡三証券|ダイヤモンド・ザイ|マン・グループ|ゴールドマン・サックス|UBS|リサーチ・アフィリエイツ|SMBC日興証券|大和証券|四季報|東証", body))
print(f"\n[出典] 出典マーカー {sc}回 {sc/man:.1f}/万字 / 社名の内訳: " + ", ".join(f"{k}{v}" for k,v in named.most_common()))
act = len(re.findall(r"ください", body))
print(f"[行動指示] 「ください」{act}回 {act/man:.1f}/万字")
boku = len(re.findall(r"僕は|僕も|僕の", body)); bokutachi = len(re.findall(r"僕たち", body))
print(f"[語り手] 「僕は/僕も/僕の」{boku}回 {boku/man:.1f}/万字 / 「僕たち」{bokutachi}回")

# ---- 主語の重心
print("\n[主語の重心 /万字]")
for k, pat in [("日本", r"日本"), ("アメリカ", r"アメリカ|米国"), ("金利・国債", r"金利|国債"), ("AI", r"AI"), ("日経平均", r"日経平均"), ("TOPIX", r"TOPIX"), ("海外", r"海外")]:
    c = len(re.findall(pat, body)); print(f"  {k:<6} {c:>4}回 {c/man:6.1f}")

# ---- 日本企業名
jp = r"キオクシア|日本マクドナルド|マクドナルド|セリア|トライアル|ワークマン|ナカニシ|上村工業|精工技研|東映アニメーション|ヨネックス|沖縄セルラー|タイミー|freee|フェローテック|QDレーザ|パワーエックス|千代田化工|アストロスケール|Synspective|ティアフォー|三洋化成|新日本建設|ブロードリーフ|東芝|TDK|豊田通商|東レ|三菱電機|シンニホンコム|ユニオンサイト|トライサット"
us = r"エヌビディア|マイクロソフト|グーグル|アマゾン|メタ|アップル|オープンAI|テスラ|ベインキャピタル"
jc = len(re.findall(jp, body)); uc = len(re.findall(us, body))
print(f"\n[企業名] 日本企業名 {jc}回 {jc/man:.1f}/万字 / 海外企業名 {uc}回 {uc/man:.1f}/万字")
print("  ブロック別 日本企業名: " + " / ".join(f"{b[0][:6]}{len(re.findall(jp, ''.join(b[1])))}" for b in blocks))

# ---- 用語説明の着地
terms = list(re.finditer(r"とは、|というのは|と呼ばれます|と呼びます|正式には|思ってください|という言葉|のことです|という約束で", body))
land = 0
for m in terms:
    seg = body[m.end(): m.end()+300]
    if re.search(jp + r"|日経平均|TOPIX", seg): land += 1
print(f"\n[説明の着地] 用語説明マーカー {len(terms)}箇所 {len(terms)/man:.1f}/万字 / 300字以内に持ち株(日本企業名・日経平均・TOPIX)が出る率 {100*land/max(len(terms),1):.0f}%")

# ---- 銘柄名簿の符号
plus = len(re.findall(r"(上昇|上げ|増え|高くな|倍にな)", body));
pp_ = len(re.findall(r"[0-9]+(?:\.[0-9]+)?%の上昇|およそ[0-9.]+倍|[0-9.]+倍にな|[0-9]+割(?:以上)?(?:上げ|高く|増え)", body))
mm_ = len(re.findall(r"[0-9]+(?:\.[0-9]+)?%の下落|[0-9]+(?:\.[0-9]+)?%下げ|[0-9]+割(?:下げ|安|減)|[0-9]+%(?:減|下回)", body))
print(f"\n[名簿の符号] プラスN%の提示 {pp_}件 / マイナスN%の提示 {mm_}件")

# ---- 繰り返し
print("\n[決まり文句] " + " / ".join(f"{k}{len(re.findall(k, body))}" for k in ["いちばん大事なところです","さきほど","正直にお伝えします","気のせいではありません","つまり","ところが","ただし","ただ、","だからこそ","もちろん"]))
