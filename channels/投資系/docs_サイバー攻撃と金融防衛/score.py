# -*- coding: utf-8 -*-
"""サイバー攻撃と金融防衛（5社）台本：伸びた型10項目＋失敗パターン＋禁止項目の一括チェック"""
import re, sys, io
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r"C:\Users\genki\01_YouTube\channels\投資系\docs_サイバー攻撃と金融防衛\scenario_draft.md"
BLK = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭'

raw = open(P, encoding='utf-8').read().split('\n')
blocks, order, cur, heads = {}, [], None, {}
for ln in raw:
    m = re.match(r'^## ([%s])\s*(.*)' % BLK, ln)
    if m:
        cur = m.group(1); blocks[cur] = []; order.append(cur); heads[cur] = m.group(2); continue
    if cur is None: continue
    if ln.startswith('>') or ln.startswith('#') or ln.startswith('---') or ln.startswith('|') or not ln.strip(): continue
    blocks[cur].append(ln.strip())

def n(s): return len(re.sub(r'\s', '', s))
full = ''.join(''.join(v) for v in blocks.values())
total = n(full)
paras = [p for b in order for p in blocks[b]]
per = lambda c: c / total * 10000

def pos_of(word):
    p = 0
    for b in order:
        for para in blocks[b]:
            i = para.find(word)
            if i >= 0: return (p + i) / total * 100
            p += n(para)
    return None

print('本文 %d 字（読み上げ約%d分）／ ブロック %d' % (total, round(total/360), len(order)))
print('\n【ブロック別】')
pos = 0
for b in order:
    c = n(''.join(blocks[b]))
    print('  %s %5d字  %4.1f〜%4.1f%%  段落%2d（平均%3d字）  %s' % (b, c, pos/total*100, (pos+c)/total*100, len(blocks[b]), c//max(1,len(blocks[b])), heads[b][:30]))
    pos += c

print('\n' + '='*70 + '\n【A】伸びた要素 10項目\n' + '='*70)
rows = []
YOB = ['あなた','ご自分','皆さん','持ち株','方もいる','という方','方なら','ください']
yob_by_block = {b: sum(1 for p in blocks[b] for w in YOB if w in p) for b in order}
zero = [b for b in order if yob_by_block[b] == 0]
rows.append(('1 視聴者への呼びかけ', '全ブロック1回以上', '空白ゼロ' if not zero else '0回: '+'・'.join(zero), not zero))
KIBOU = ['覇権','主役','欠かせ','追い風','強み','チャンス']
k = sum(full.count(w) for w in KIBOU)
rows.append(('2 希望語', '10回/万字以上', '%.1f回/万字（%d回）%s' % (per(k), k, dict(Counter(w for w in KIBOU if full.count(w)) ) ), per(k) >= 10))
SHU = ['KPMG','IMF','FRB','日銀','金融庁','FBI','司法省','クラウドストライクの調査','パロアルトネットワークスが','グーグルのセキュリティ','会社四季報','決算','統合報告書','報告書','説明会','ブログ','Binanceは','デジタル庁は','楽天証券は']
s = sum(full.count(w) for w in SHU)
rows.append(('3 出典の密度', '10回/万字以上', '%.1f回/万字（%d回）' % (per(s), s), per(s) >= 10))
a = full.count('ください')
rows.append(('4 行動指示', '3.4〜3.8回/万字', '%.1f回/万字（%d回）' % (per(a), a), per(a) >= 3.4))
sub = sum(1 for ln in raw if ln.startswith('### '))
rows.append(('5 小見出し', '11個以上', '%d個（##も含め %d）' % (sub, sub+len(order)), sub+len(order) >= 11))
avg = total/len(paras)
rows.append(('6 段落の平均', '100字以内', '%.0f字（最長%d字・100字超%d段落）' % (avg, max(n(p) for p in paras), sum(1 for p in paras if n(p)>100)), avg <= 100))
MEI = ['マクニカ','ベイカレント','野村総合研究所','テクマトリックス','オプテックス']
HIG = ['GMO','デジタル庁','skyticket','NEC','Binance','DMM']
first_any = min(x for x in [pos_of(w) for w in MEI+HIG] if x is not None)
first_mei = min(x for x in [pos_of(w) for w in MEI] if x is not None)
rows.append(('7 社名の初出', '10%まで（マクロ軸は1社フルでも可）', '被害企業含む %.1f%% ／ 銘柄 %.1f%%' % (first_any, first_mei), first_mei <= 11))
fm = pos_of('証券コードは3132')
rows.append(('8 数字つき銘柄（1社フル）の初出', '32%まで', '%.1f%%' % fm, fm <= 32))
ap = pos_of('不安になるのは当然')
rows.append(('9 痛みの承認の位置', '15%まで', '%.1f%%' % ap, ap <= 15))
b_ = full.count('僕')
rows.append(('10 「僕」', '少ないほどよい', '%d回' % b_, True))
for name, tgt, val, ok in rows:
    print('  %s %-24s 目標 %-16s %s' % ('○' if ok else '✕', name, tgt, val))

print('\n' + '='*70 + '\n【B】伸びなかった2本の失敗パターン\n' + '='*70)
op = ''.join(blocks[order[0]])
neg = len(re.findall(r'ません|ありません|ではない|ていない|いけません|限りません|足りません', full))
fut = len(re.findall(r'20(3[0-9]|4[0-9])年', full))
riyu = ''.join(''.join(blocks[b]) for b in ['⑤','⑥','⑦'] if b in blocks)
jp = riyu.count('日本'); jpco = sum(riyu.count(w) for w in MEI)
fgco = sum(riyu.count(w) for w in ['OpenAI','マイクロソフト','Anthropic','パロアルトネットワークス','クラウドストライク','Binance','グーグル'])
bad = [
 ('冒頭が短く要素不足', '%d字' % n(op), n(op) >= 600),
 ('小見出しゼロ', '%d個' % sub, sub > 0),
 ('段落が長い（平均177字）', '平均%.0f字' % avg, avg <= 100),
 ('呼びかけの空白', '欠けなし' if not zero else '欠けあり', not zero),
 ('否定で押し通す（108.6回/万字）', '%.0f回/万字' % per(neg), per(neg) <= 90),
 ('遠い未来の年号（4.6回/万字）', '%.1f回/万字（%d回）' % (per(fut), fut), per(fut) <= 2.5),
 ('理由の主役が海外企業', '⑤⑥⑦で 日本%d・日本企業%d / 海外企業%d' % (jp, jpco, fgco), jp+jpco >= fgco),
]
for name, val, ok in bad:
    print('  %s %-28s いま=%s' % ('○' if ok else '✕', name, val))
mixed = [p for p in paras if re.search(r'[0-9]割|[0-9]+%|[0-9]倍', p) and 'マイナス' in p and ('増え' in p or '超え' in p)]
print('  %s 勝ち負けの混在（上げと下げを同じ段落に）: %d件' % ('○' if not mixed else '△', len(mixed)))
for p in mixed: print('      ', p[:80])

print('\n' + '='*70 + '\n【C】禁止項目・上限（CLAUDE.md §1・§6）\n' + '='*70)
body_lines = [ln for ln in raw if not ln.startswith('>')]
def cnt(pat, text=full): return len(re.findall(pat, text))
checks = [
 ('「私」', cnt('私'), 0),
 ('「〜のです。」', cnt(r'[^も]のです。'), 0),
 ('本文の強調太字', sum(1 for ln in body_lines if not ln.startswith('#') and '**' in ln), 0),
 ('「会社」（四季報・証券会社・運用会社を除く）', cnt('会社', re.sub('会社四季報|証券会社|運用会社','',full)), 0),
 ('普段使いしない言い回し', cnt('局面|筋道|側面が強い|見方を示し|物差し|景色|示唆|運用が続く'), 0),
 ('方向の断定・推奨語', cnt('買い場|狙い目|ねらい目|仕込み時|割安|買ってみ|買う前|買うなら|買い時|おすすめ|お勧め'), 0),
 ('相対的な時間', cnt('先週|今週|今月|先月|昨日|直近で|最近|この秋'), 0),
 ('たとえ話', cnt('ようなもの|だと思ってください|想像してください|たとえば'), 0),
 ('書き手の用語', cnt('伏線|回収|実践です'), 0),
 ('「犯人」', cnt('犯人'), None),
]
for name, c, lim in checks:
    ok = (lim is None) or c <= lim
    print('  %s %-32s %d件%s' % ('○' if ok else '✕', name, c, '' if lim is None else '（上限%d）' % lim))
print('\n  繰り返しの上限')
for k_, lim in [('ここがいちばん大事なところです',1),('さきほどお話ししたとおり',2),('正直にお伝えします',3),('気のせいではありません',1),('の整理では',1),('最初にお伝えした',3),('さきほど',8),('ここで、',4),('つまり、',8),('では、',10)]:
    c = full.count(k_)
    print('    %s %-20s %d回（目安%d）' % ('○' if c <= lim else '△', k_, c, lim))
pre = cnt('このあと|あとで')
print('    %s 「このあと／あとで」の予告 %d回（上限 1万字6回＝%d回）' % ('○' if pre <= total/10000*6 else '✕', pre, int(total/10000*6)))
print('    「日本でいえば」 %d回 ／ 「ROEというのは」 %d回（1回だけ） ／ 「ETFというのは」 %d回' % (full.count('日本でいえば'), full.count('ROEというのは'), full.count('ETFというのは')))

print('\n  同じ固有名詞の説明の重複')
for w in ['IMF', 'FRBは', 'GPIF', 'KPMGジャパン', 'アクセンチュア', 'クラウドストライク', 'パロアルトネットワークス', 'ノルウェーの政府の基金', 'ほふり', '日本証券業協会']:
    print('    %-18s %d回' % (w, full.count(w)))

print('\n【D】数字の点呼（1段落に数字が5個以上）')
for b in order:
    for p in blocks[b]:
        c = len(re.findall(r'[0-9０-９][0-9０-９,\.]*', p))
        if c >= 7: print('  %s %d個: %s…' % (b, c, p[:70]))

print('\n【E】重複しやすい文（同じ30字以上の文が2回出ていないか）')
sents = re.split(r'(?<=。)', full)
cc = Counter(s_ for s_ in sents if n(s_) >= 25)
for s_, c in cc.items():
    if c > 1: print('  %d回: %s' % (c, s_[:60]))
print('  （出力なしなら重複なし）')
