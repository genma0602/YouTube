# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = r"C:\Users\genki\01_YouTube\channels\投資系\docs_サイバーセキュリティ\scenario_draft.md"
PLANNED_TOTAL = 17600  # 完成見込み（10/7 実測から再計算：①〜⑤が計画の79%で収まった）

raw = open(PATH, encoding='utf-8').read().split('\n')

# 本文だけ（注記 > 行、見出し、罫線、表を除く）
blocks = {}   # id -> list of paragraph strings
cur = None
buf = []
order = []
for ln in raw:
    m = re.match(r'^## ([①②③④⑤⑥⑦⑧⑨⑩⑪])', ln)
    if m:
        cur = m.group(1); blocks[cur] = []; order.append(cur); continue
    if cur is None: continue
    if ln.startswith('>') or ln.startswith('#') or ln.startswith('---') or ln.startswith('|'):
        continue
    if ln.strip() == '':
        continue
    blocks[cur].append(ln.strip())

def n(s): return len(re.sub(r'\s', '', s))

full = ''.join(''.join(p) for p in blocks.values())
total = n(full)
paras = [p for b in order for p in blocks[b]]

print('=' * 64)
print('現状：ブロック %s ／ 本文 %d 字（完成見込み %d 字の %.1f%%）' % ('・'.join(order), total, PLANNED_TOTAL, total/PLANNED_TOTAL*100))
print('=' * 64)

# --- ブロック別・位置 ---
print('\n【ブロック別】')
pos = 0
spans = {}
for b in order:
    c = n(''.join(blocks[b]))
    spans[b] = (pos, pos + c)
    print('  %s  %5d字   完成時の位置 %4.1f%% 〜 %4.1f%%   段落%d（平均%d字）'
          % (b, c, pos/PLANNED_TOTAL*100, (pos+c)/PLANNED_TOTAL*100,
             len(blocks[b]), c//max(1, len(blocks[b]))))
    pos += c

print('\n【段落】 %d段落 ／ 平均 %.0f字 ／ 最長 %d字 ／ 100字超 %d段落（%.0f%%）／ 150段落per万字 換算 %.0f'
      % (len(paras), total/len(paras), max(n(p) for p in paras),
         sum(1 for p in paras if n(p) > 100), sum(1 for p in paras if n(p) > 100)/len(paras)*100,
         len(paras)/total*10000))

# --- 指標 ---
def find_all(words):
    hits = []
    p = 0
    for b in order:
        for para in blocks[b]:
            for w in words:
                for m in re.finditer(re.escape(w), para):
                    hits.append((b, p + m.start(), w))
            p += n(para)
    return sorted(hits, key=lambda x: x[1])

YOBIKAKE_STRICT = ['あなた', 'ご自分', '皆さん', '持ち株']
YOBIKAKE_LOOSE  = YOBIKAKE_STRICT + ['方もいる', 'という方', 'ください', 'みてください']
KIBOU = ['覇権', '主役', '欠かせな', '追い風', '強み', 'チャンス', '本番']
SHUTTEN = ['警察庁', 'JIPDEC', 'Anthropic', '会社四季報', 'ロイター', '日本経済新聞',
           'モルガン・スタンレー', 'ブラックロック', 'IDC', 'ガートナー', 'Omdia',
           'ウェドブッシュ', 'ローゼンブラット', 'FBI', '決算資料']
MEIGARA = ['ソリトンシステムズ', 'サイバーセキュリティクラウド', 'FFRIセキュリティ',
           'トレンドマイクロ', 'デジタルアーツ', 'ZenmuTech', 'カウリス',
           'セキュアヴェイル', 'ブロードバンドセキュリティ']
HIGAI = ['焼肉きんぐ', '大和証券', 'タイムズカー', 'パーク24', 'アサヒグループホールディングス', '山一電機']
KATAKANA = ['ランサムウェア', 'アカウント', 'システム', 'ネットワーク', 'アプリ', 'データ',
            'サーバー', 'パスワード', 'ウェブ', 'クラウド', 'アクセス', 'セキュリティ']

def report(label, words, target=None, strict_list=False):
    hits = find_all(words)
    per = len(hits) / total * 10000
    t = '' if target is None else '   目標 %s' % target
    print('\n【%s】 %d回 ／ 1万字あたり %.1f回%s' % (label, len(hits), per, t))
    return hits

h = report('希望語', KIBOU, '10回/万字以上（伸びず組 2.7〜3.1）')
from collections import Counter
print('   内訳:', dict(Counter(w for _, _, w in h)))
print('   ブロック別:', dict(Counter(b for b, _, _ in h)))

h = report('出典名', SHUTTEN, '10回/万字以上（伸びた7万円版 10.1）')
print('   内訳:', dict(Counter(w for _, _, w in h)))

h = report('行動指示（ください）', ['ください'], '3.4〜3.8回/万字')
h = report('カタカナ専門語', KATAKANA, '伸びた版 10.3〜19.6回/万字（避けすぎない）')

print('\n【呼びかけ】')
hs = find_all(YOBIKAKE_STRICT)
print('   厳密（あなた/ご自分/皆さん/持ち株）: %d回' % len(hs))
for b in order:
    c = sum(1 for x in hs if x[0] == b)
    print('     %s: %d回 %s' % (b, c, '← 0回' if c == 0 else ''))
hl = find_all(YOBIKAKE_LOOSE)
print('   広め（＋「〜という方」「ください」）: %d回' % len(hl))
for b in order:
    print('     %s: %d回' % (b, sum(1 for x in hl if x[0] == b)))
if hs:
    first = hs[0][1]
    print('   初出 %d字目 ＝ 完成時の %.1f%% 地点（冒頭からの空白 %.1fpt）' % (first, first/PLANNED_TOTAL*100, first/PLANNED_TOTAL*100))
    gaps = [0] + [x[1] for x in hl]
    mx = max(gaps[i+1]-gaps[i] for i in range(len(gaps)-1))
    print('   広めでの最長空白 %d字 ＝ %.1fpt（目標 40pt以内）' % (mx, mx/PLANNED_TOTAL*100))

print('\n【社名】')
hm = find_all(MEIGARA)
hh = find_all(HIGAI)
if hm:
    print('   銘柄（守る側）: %d回 ／ 初出 %d字目 ＝ %.1f%%' % (len(hm), hm[0][1], hm[0][1]/PLANNED_TOTAL*100))
    print('     ', dict(Counter(w for _, _, w in hm)))
if hh:
    print('   被害企業: %d回 ／ 初出 %d字目 ＝ %.1f%%' % (len(hh), hh[0][1], hh[0][1]/PLANNED_TOTAL*100))
    print('     ', dict(Counter(w for _, _, w in hh)))
allname = sorted(hm + hh, key=lambda x: x[1])
print('   社名ぜんぶの初出 %.1f%% ／ 伸びた3本は10%%まで' % (allname[0][1]/PLANNED_TOTAL*100))

# 数字つき銘柄の初出（銘柄名の前後120字に数字）
num_first = None
for b, p, w in hm:
    seg = full[max(0, p-60):p+120]
    if re.search(r'[0-9０-９]', seg):
        num_first = (w, p); break
if num_first:
    print('   数字つき銘柄の初出: %s ＝ %.1f%%（伸びた3本は32%%まで）' % (num_first[0], num_first[1]/PLANNED_TOTAL*100))

print('\n【そのほか】')
print('   「僕」: %d回（1万字あたり %.1f。伸びず組 5.8）' % (full.count('僕'), full.count('僕')/total*10000))
neg = len(re.findall(r'ません|ありません|ではない|ていない|届きません|限りません', full))
print('   否定形: %d回 ／ 1万字あたり %.0f（伸びた版 64〜86、AI半導体版 108）' % (neg, neg/total*10000))
print('   小見出し: %d個（目標 11個以上。現在③のみ）' % sum(1 for ln in raw if ln.startswith('### ')))
print('   文の数: %d ／ 平均文長 %.0f字（伸びた版 31〜37字）'
      % (len(re.findall(r'[。]', full)), total/max(1, len(re.findall(r'[。]', full)))))
