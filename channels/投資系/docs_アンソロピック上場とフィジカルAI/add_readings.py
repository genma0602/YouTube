# -*- coding: utf-8 -*-
# scenario_本文のみ.md → scenario_本文のみ_Googleドキュメント用.md（機関名・企業名・商品名の最初の1回に「表記(読み)」を入れる）
# 読み方の表は readings.tsv。題名の行には入れない。スライドの元（scenario_本文のみ.md）は読みなしのまま。G7財政危機の add_readings.py と同じ
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
D = r"C:\Users\genki\01_YouTube\channels\投資系\docs_アンソロピック上場とフィジカルAI"
src = io.open(D + r"\scenario_本文のみ.md", encoding="utf-8").read().split("\n")
pairs = []
for ln in io.open(D + r"\readings.tsv", encoding="utf-8"):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("#"):
        continue
    k, v = ln.split("\t")
    pairs.append((k, v))

done = set()
out = []
for line in src:
    if line.startswith("#"):
        out.append(line); continue
    for k, v in pairs:
        if k in done:
            continue
        longer = [kk for kk, _ in pairs if kk != k and k in kk]
        pat = re.escape(k)
        for lk in longer:
            a, b = lk.split(k, 1)
            if a: pat = "(?<!" + re.escape(a) + ")" + pat
            if b: pat = pat + "(?!" + re.escape(b) + ")"
        if k.isascii():
            pat = r"(?<![A-Za-z0-9])" + pat + r"(?![A-Za-z0-9(])"
        m = re.search(pat, line)
        if m:
            line = line[:m.start()] + k + "(" + v + ")" + line[m.end():]
            done.add(k)
    out.append(line)
missing = [k for k, _ in pairs if k not in done]
io.open(D + r"\scenario_本文のみ_Googleドキュメント用.md", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("読みを入れた:", len(done), "/ 本文に無かった:", missing)
for line in out:
    for m in re.finditer(r"[^\s、。「」（）()]*\([^()]+\)", line):
        print("  ", m.group(0))
