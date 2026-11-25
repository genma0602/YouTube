# -*- coding: utf-8 -*-
"""伸びた要素／伸びなかった要素の両面チェック"""
import re, sys, io
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r"C:\Users\genki\01_YouTube\channels\投資系\docs_サイバーセキュリティ\scenario_draft.md"
TOTAL_EST = 17600

raw = open(P, encoding='utf-8').read().split('\n')
blocks, order, cur = {}, [], None
for ln in raw:
    m = re.match(r'^## ([①②③④⑤⑥⑦⑧⑨⑩⑪])', ln)
    if m:
        cur = m.group(1); blocks[cur] = []; order.append(cur); continue
    if cur is None: continue
    if ln.startswith('>') or ln.startswith('#') or ln.startswith('---') or not ln.strip(): continue
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
            if i >= 0: return (p + i) / TOTAL_EST * 100
            p += n(para)
    return None

print('書いた範囲：%s（%d字 ／ 完成見込み %d字の %.1f%%）' % ('〜'.join([order[0], order[-1]]), total, TOTAL_EST, total/TOTAL_EST*100))

print('\n' + '='*70)
print('【A】伸びた要素 ── 入っているか')
print('='*70)

rows = []
# 1 呼びかけ
YOB = ['あなた','ご自分','皆さん','持ち株']
yob_by_block = {b: sum(1 for p in blocks[b] for w in YOB if w in p) for b in order}
zero = [b for b in order if yob_by_block[b] == 0]
rows.append(('1 視聴者への呼びかけ', '全ブロックに1回以上', '各1回（空白ゼロ）' if not zero else '0回のブロック: '+'・'.join(zero), not zero))
# 2 希望語
KIBOU = ['覇権','主役','欠かせな','追い風','強み','チャンス','本番']
k = sum(full.count(w) for w in KIBOU)
rows.append(('2 希望語', '10回/万字以上', '%.1f回/万字（%d回）' % (per(k), k), per(k) >= 10))
# 3 出典
SHU = ['警察庁','JIPDEC','Anthropic','会社四季報','決算資料','FBI','モルガン・スタンレー',
       'フォーチュン・ビジネス・インサイツ','ソフトバンクグループ','OpenAI']
s = sum(full.count(w) for w in SHU)
rows.append(('3 出典の密度', '10回/万字以上', '%.1f回/万字（%d回）' % (per(s), s), per(s) >= 10))
# 4 行動指示
a = full.count('ください')
rows.append(('4 行動指示', '3.4〜3.8回/万字', '%.1f回/万字（%d回）' % (per(a), a), per(a) >= 3.4))
# 5 小見出し
sub = sum(1 for ln in raw if ln.startswith('### '))
rows.append(('5 小見出し', '11個以上（最終）', '%d個' % sub, sub >= 11))
# 6 段落
avg = total/len(paras)
rows.append(('6 段落の平均', '100字以内', '%.0f字（最長%d字）' % (avg, max(n(p) for p in paras)), avg <= 100))
# 7 社名の初出
MEI = ['ソリトンシステムズ','サイバーセキュリティクラウド','FFRIセキュリティ']
HIG = ['焼肉きんぐ','大和証券','タイムズカー','パーク24','アサヒグループホールディングス','山一電機']
first_any = min(x for x in [pos_of(w) for w in MEI+HIG] if x is not None)
rows.append(('7 社名の初出', '10%まで', '%.1f%%' % first_any, first_any <= 10))
# 8 数字つき銘柄
fm = pos_of('ソリトンシステムズ')
rows.append(('8 数字つき銘柄の初出', '32%まで', '%.1f%%' % fm, fm <= 32))
# 9 承認の位置
ap = pos_of('気のせいではありません')
rows.append(('9 痛みの承認の位置', '15%まで', '%.1f%%' % ap, ap <= 15))
# 10 「僕は」
b_ = full.count('僕')
rows.append(('10 「僕」で逃げない', '少ないほどよい', '%d回' % b_, True))

for name, tgt, val, ok in rows:
    print('  %s %-22s 目標 %-18s %s' % ('○' if ok else '✕', name, tgt, val))

print('\n' + '='*70)
print('【B】伸びなかった要素 ── 排除できているか')
print('='*70)
print('\n--- 日米同時利上げ（伸びず）の失敗パターン ---')
op = ''.join(blocks[order[0]])
bad = []
bad.append(('冒頭が短く要素不足', '316字・迷いなし・結論先出しなし', '%d字' % n(op), n(op) >= 600))
bad.append(('社名の初出が遅い', '43.2%', '%.1f%%' % first_any, first_any <= 10))
bad.append(('数字つき銘柄が遅い', '53.8%', '%.1f%%' % fm, fm <= 32))
bad.append(('小見出しゼロ', '0個', '%d個' % sub, sub > 0))
bad.append(('行動指示ほぼゼロ', '0.5回/万字', '%.1f回/万字' % per(a), per(a) >= 3.4))
bad.append(('段落が長い', '平均177字', '平均%.0f字' % avg, avg <= 100))
bad.append(('呼びかけの空白', '84.4pt', '0ブロック欠け' if not zero else '欠けあり', not zero))
for name, ng, val, ok in bad:
    print('  %s %-20s 伸びず組=%-16s いま=%s' % ('○' if ok else '✕', name, ng, val))

print('\n--- AI半導体バブル（伸びず）の失敗パターン ---')
bad2 = []
bad2.append(('中盤で話しかけない', '本文73%まで呼びかけ0', '全ブロックに1回' if not zero else '欠けあり', not zero))
bad2.append(('希望語が少ない', '2.7回/万字', '%.1f回/万字' % per(k), per(k) >= 10))
bad2.append(('承認が終盤', '74.0%地点', '%.1f%%地点' % ap, ap <= 15))
neg = len(re.findall(r'ません|ありません|ではない|ていない|いけません|限りません|足りません', full))
bad2.append(('否定で押し通す', '108.6回/万字', '%.0f回/万字' % per(neg), per(neg) <= 90))
fut = len(re.findall(r'20(3[0-9]|4[0-9])年', full))
bad2.append(('遠い未来の年号', '4.6回/万字', '%.1f回/万字（%d回）' % (per(fut), fut), per(fut) <= 2.5))
# 理由パートの主語
riyu = ''.join(''.join(blocks[b]) for b in ['⑤','⑥','⑦'] if b in blocks)
rn = n(riyu)
jp = riyu.count('日本')
jpco = sum(riyu.count(w) for w in ['ソリトンシステムズ','サイバーセキュリティクラウド','FFRIセキュリティ','ソフトバンクグループ'])
fgco = sum(riyu.count(w) for w in ['OpenAI','マイクロソフト','Anthropic','パロアルトネットワークス',
                                   'クラウドストライク','フォーティネット','ゼットスケーラー','モルガン・スタンレー'])
bad2.append(('理由の主役が海外企業', '海外ビッグテックが主役', '理由パート（⑤⑥⑦ %d字）で 日本%d回・日本企業%d回 / 海外企業%d回' % (rn, jp, jpco, fgco), jp + jpco >= fgco))
for name, ng, val, ok in bad2:
    print('  %s %-20s 伸びず組=%-18s いま=%s' % ('○' if ok else '✕', name, ng, val))

print('\n--- 勝ち負けの混在（7万円版が避け、AI半導体版が踏んだ） ---')
mixed = [p for p in paras if re.search(r'[0-9]割|[0-9]+%|[0-9]倍', p) and 'マイナス' in p and ('増え' in p or '超え' in p)]
print('  %s 同じ段落に上げと下げを混ぜた箇所: %d件' % ('○' if not mixed else '△', len(mixed)))
for p in mixed: print('     ', p[:90], '…')
print('  ※⑦のゼットスケーラーは承認パート（米国株）に閉じてある。日本株の名簿は⑨でまだ未着手')

print('\n' + '='*70)
print('【C】効かないと分かっているもの（気にしなくてよい）')
print('='*70)
tatoe = len(re.findall(r'ようなもの|だと思ってください|想像して|たとえば', full))
print('  たとえ話: %d回（%.1f回/万字）── 最少の7万円版がいちばん伸びた。増やす必要なし' % (tatoe, per(tatoe)))
print('  平均文長: %.0f字 ── 伸びた版31〜37字。短くしても伸びには寄与しない' % (total/len(re.findall(r'。', full))))
longest = max((n(''.join(blocks[b])), b) for b in order)
print('  最長ブロック: %s（全体の%.1f%%）── 7万円版は48%%の単独ブロックで伸びた。均等割りは正解でない' % (longest[1], longest[0]/total*100))
