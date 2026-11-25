# -*- coding: utf-8 -*-
# scenario_draft.md → scenario_本文のみ.md（注記・区切り線・表を除いた本文）
#                   → scenario_本文のみ_Googleドキュメント用.md（英語表記の機関名・企業名・商品名の最初の1回に「表記(読み)」）
# 読み方の表は readings.tsv。題名の行には入れない。scenario_draft.md と scenario_本文のみ.md は読みなしのまま
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
D = r"C:\Users\genki\01_YouTube\channels\投資系\docs_米中間選挙"
TITLE = "米中間選挙のあと、日米の株価はどうなるのか。11月に決算を迎える日本の優良株11社（仮）"

lines = io.open(D + r"\scenario_draft.md", encoding="utf-8").read().split("\n")
body = ["# " + TITLE]
started = False
for ln in lines:
    s = ln.rstrip()
    if s.startswith("## "):
        started = True
    if not started or not s.strip():
        continue
    if s.startswith((">", "---", "|", "# ")):
        continue
    body.append(s)
io.open(D + r"\scenario_本文のみ.md", "w", encoding="utf-8", newline="\n").write("\n\n".join(body) + "\n")

pairs = []
for ln in io.open(D + r"\readings.tsv", encoding="utf-8"):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("#"):
        continue
    k, v = ln.split("\t")
    pairs.append((k, v))

done = set()
out = []
for line in body:
    if line.startswith("# "):
        out.append(line); continue
    for k, v in pairs:
        if k in done:
            continue
        # 長い名前の一部としての出現（PlayStation 5 の中の PlayStation）は対象外
        pat = re.escape(k)
        for lk, _ in pairs:
            if lk != k and k in lk:
                a, b = lk.split(k, 1)
                if a: pat = "(?<!" + re.escape(a) + ")" + pat
                if b: pat = pat + "(?!" + re.escape(b) + ")"
        if k[0].isascii():
            pat = r"(?<![A-Za-z])" + pat
        if k[-1].isascii():
            pat = pat + r"(?![A-Za-z(])"
        m = re.search(pat, line)
        if m:
            line = line[:m.end()] + "(" + v + ")" + line[m.end():]
            done.add(k)
    out.append(line)
io.open(D + r"\scenario_本文のみ_Googleドキュメント用.md", "w", encoding="utf-8", newline="\n").write("\n\n".join(out) + "\n")
print("読みを入れた:", len(done), "/ 本文に無かった:", [k for k, _ in pairs if k not in done])
left = sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9&.\- ]*[A-Za-z0-9]", "\n".join(out))))
print("残った英字:", left)
