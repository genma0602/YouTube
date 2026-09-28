import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def blocks_of(path):
    raw = open(path, encoding="utf-8").read().split("\n")
    out = []; cur = None
    for ln in raw:
        if ln.startswith("## "):
            cur = [ln[3:].strip(), []]; out.append(cur); continue
        if cur is None: continue
        if ln.startswith(("#", ">", "---", "|")) or not ln.strip(): continue
        cur[1].append(ln.strip())
    return out

NUM = re.compile(r"[0-9０-９][0-9０-９,\.]*")
ENUM = re.compile(r"[0-9０-９]+つ目|[0-9０-９]+つ|[0-9０-９]+点|[0-9０-９]+種類|[0-9０-９]+社の")  # 目次・列挙の番号
DATE = re.compile(r"[0-9０-９]+月[0-9０-９]*日?|[0-9０-９]{4}年")

def stats(title, text):
    n = len(text)
    nums = NUM.findall(text)
    enum = len(re.findall(r"[0-9０-９]+つ目|[0-9０-９]つ", text))
    dates = len(DATE.findall(text))
    data = len(nums) - enum - dates
    print(f"  {title[:26]:<28} {n:>5}字  数字{len(nums):>3}（目次・列挙{enum:>2}／日付{dates:>2}／データ{max(data,0):>3}）  データ密度 {100*max(data,0)/n:4.1f}/100字")

for label, path, want in [
    ("7万円（伸びた）", "台本/【日経平均7万円突破！】米国・イラン終戦で日本株に歴史的チャンス到来？.md", ["①","②","③"]),
    ("10万円（伸びた）", "台本/【日経平均10万円は近い？】日本株はバブルなのか⁉AI半導体の覇権は日本！日本株はもう下がらない！【TOPIX／オルカン／S＆P500／NASDAQ100／FANG+】.md", ["①","②","③"]),
    ("TOPIX改革（現在）", "docs_TOPIX改革/scenario_draft.md", ["①","②"]),
]:
    print(f"\n[{label}]")
    for t, pars in blocks_of(path):
        if any(t.startswith(w) for w in want):
            stats(t, "".join(pars))

print("\n[私の案]")
old = open(sys.argv[1], encoding="utf-8").read()
new = open(sys.argv[2], encoding="utf-8").read()
stats("昨日の案（②の頭）", old.replace("\n",""))
stats("縮めた案（②の頭）", new.replace("\n",""))
