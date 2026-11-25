# -*- coding: utf-8 -*-
# scenario_本文のみ_Googleドキュメント用.md → 同名の .docx（見出しつき・游ゴシック11pt）。Googleドライブに上げて開く用
import io, sys
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
D = r"C:\Users\genki\01_YouTube\channels\投資系\docs_アンソロピック上場とフィジカルAI"
src = io.open(D + r"\scenario_本文のみ_Googleドキュメント用.md", encoding="utf-8").read().split("\n")
doc = Document()
st = doc.styles["Normal"]
st.font.name = "Yu Gothic"
st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Yu Gothic")
n = 0
for line in src:
    line = line.rstrip()
    if not line:
        continue
    if line.startswith("## "):
        doc.add_heading(line[3:], 1)
    elif line.startswith("# "):
        doc.add_heading(line[2:], 0)
    else:
        doc.add_paragraph(line)
        n += 1
doc.save(D + r"\scenario_本文のみ_Googleドキュメント用.docx")
print("docx 段落", n)
