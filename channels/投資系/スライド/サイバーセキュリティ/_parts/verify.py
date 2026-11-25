# -*- coding: utf-8 -*-
"""検収チェックリスト（PLAN.md §8）の機械で確かめられる分"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
doc = io.open(os.path.join(HERE, "..", u"サイバーセキュリティ.html"), encoding="utf-8").read()
body = doc.split("<body>")[1]
text = re.sub(r"<[^>]+>", "", body)
slides = re.findall(r'<section class="slide[^"]*">(.*?)</section>', body, re.S)

ok, ng = [], []


def t(cond, msg):
    (ok if cond else ng).append(msg)


# 枚数
t(len(slides) == 301, u"スライド 301枚（実際 %d枚）" % len(slides))

# 証券コード（9社・各1回）
codes = {u"3040": u"ソリトンシステムズ", u"4493": u"サイバーセキュリティクラウド", u"3692": u"FFRIセキュリティ",
         u"4398": u"ブロードバンドセキュリティ", u"153A": u"カウリス", u"3042": u"セキュアヴェイル",
         u"338A": u"ZenmuTech", u"2326": u"デジタルアーツ", u"4704": u"トレンドマイクロ"}
for cd, nm in codes.items():
    n = len(re.findall(r'<span class="u" style="font-size:\d+px">　%s</span>' % cd, body))
    t(n == 1, u"証券コード %s（%s）が社名スライドに1回（実際 %d回）" % (cd, nm, n))

# 株価の基準日
n15 = len(re.findall(r'<div class="c-l">1月5日</div>', body))
n107 = len(re.findall(r'<div class="c-l">10月7日</div>', body))
t(n15 == 9 and n107 == 9, u"株価の図は全9社「1月5日→10月7日」（1月5日 %d／10月7日 %d）" % (n15, n107))

# 米国株の実数が出ていない
t(not re.search(r"128|138\.0|140\.9|-5\.6", text), u"米国4社の個別の騰落率を出していない")

# 設定名
t(text.count(u"ログインパスワードの無効設定") == 1, u"SBI証券「ログインパスワードの無効設定」が正確に1回")
t(text.count(u"取引やサービスの一時的な利用停止") == 1, u"楽天証券「取引やサービスの一時的な利用停止」が正確に1回")

# 禁止語
for word in [u"割安", u"買い場", u"狙い目", u"仕込み", u"私"]:
    t(word not in text, u"「%s」0件" % word)
t(not re.search(u"[^も]のです。", text), u"「〜のです。」0件（「ものです」はCLAUDE.mdどおり対象外）")
kaisha = text.replace(u"会社四季報", u"").replace(u"子会社", u"").replace(u"調査会社", u"")
t(u"会社" not in kaisha, u"「会社」0件（会社四季報・子会社・調査会社をのぞく）")
for word in [u"想像してください", u"ようなもの", u"だと思ってください"]:
    t(word not in text, u"たとえ話「%s」0件" % word)
t(not re.search(r"[+＋][0-9]+\.[0-9]+%", text), u"実数の騰落率（+39.1%など）を使っていない")

# チャンネル名
t(len(re.findall(r'<span class="brand"></span>', body)) == len(re.findall(r'<span class="brand"', body)),
  u"ヘッダー右のブランド欄はすべて空")

# 丸めた言い方が本文どおり
for phrase in [u"およそ4割", u"6割近く", u"2割近く", u"6割を超えました", u"9割を超えました",
               u"3割を超えました", u"わずかにプラス", u"1割を超えるマイナス", u"8%ほど"]:
    t(phrase in text, u"丸めた言い方「%s」がある" % phrase)

# 段階の帯
t(len(re.findall(r'class="stagemap', body)) == 15, u"stagemap が15枚（実際 %d枚）" % len(re.findall(r'class="stagemap', body)))

print(u"── 通過 %d件" % len(ok))
for m in ok:
    print(u"  ○ %s" % m)
if ng:
    print(u"\n── ★要確認 %d件" % len(ng))
    for m in ng:
        print(u"  ★ %s" % m)
else:
    print(u"\n全項目クリア")
