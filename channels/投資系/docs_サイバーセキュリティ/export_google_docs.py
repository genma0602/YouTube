# -*- coding: utf-8 -*-
"""scenario_本文のみ.md から Googleドキュメント用の .docx を作る。

    python docs_サイバーセキュリティ/export_google_docs.py

見出しの付け方（TOPIX改革・光電融合の既存ファイルと同じ）:
    #   → Title       … 動画のタイトル
    ##  → Heading 1   … ①〜⑪ のブロック
    ### → Heading 2   … 小見出し
    本文 → Normal（Yu Gothic 11pt・行間1.5）

Googleドキュメントにアップロードすると、この見出しがそのまま
左側の「ドキュメントの概要」（目次）になる。

元が変わったら、scenario_本文のみ.md を作り直してから再実行する（HANDOFF.md §11）。
"""
from pathlib import Path
import io
import re

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Pt

BASE = Path(__file__).resolve().parent
SRC = BASE / "scenario_本文のみ.md"
OUT = BASE / "scenario_本文のみ_Googleドキュメント用.docx"

# 本文の見出し（# 行）は「台本｜〜」なので、タイトルはここで決める。
# 確定したら HANDOFF.md §8 のタイトルに差し替える。
TITLE = "AI時代のサイバーセキュリティ株（仮題）"


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.replace("**", "").replace("__", "").strip()


def main() -> None:
    document = Document()
    normal = document.styles["Normal"]
    normal.font.name = "Yu Gothic"
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(10)

    counts = {"title": 0, "h1": 0, "h2": 0, "body": 0}
    chars = 0

    for raw in io.open(SRC, encoding="utf-8").read().splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip() == "---":
            continue
        if line.startswith(">"):            # 要検証メモ（念のため）
            continue

        heading = re.fullmatch(r"(#{1,3})\s+(.+)", line)
        if heading:
            level, text = len(heading.group(1)), clean_inline(heading.group(2))
            if level == 1:                  # 台本のタイトル行は、動画のタイトルに差し替える
                document.add_heading(TITLE, 0)
                counts["title"] += 1
            else:
                document.add_heading(text, level - 1)
                counts["h1" if level == 2 else "h2"] += 1
            continue

        body = clean_inline(line)
        document.add_paragraph(body)
        counts["body"] += 1
        chars += len(re.sub(r"\s", "", body))

    footer = document.sections[0].footer.paragraphs[0]
    footer.add_run("Googleドキュメントへアップロードして編集できます。")
    footer.add_run().add_break(WD_BREAK.LINE)
    footer.add_run("作成元: %s" % SRC.name)

    document.save(OUT)

    print("出力: %s" % OUT.name)
    print("タイトル %d / 見出し1 %d / 見出し2 %d / 本文 %d段落"
          % (counts["title"], counts["h1"], counts["h2"], counts["body"]))
    print("本文の字数: %d" % chars)


if __name__ == "__main__":
    main()
