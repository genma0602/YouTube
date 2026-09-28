from pathlib import Path
import re
import sys

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Pt


DEFAULT_SOURCE = Path(
    r"c:\Users\genki\01_YouTube\channels\投資系\台本\【日経平均10万円は近い？】日本株はバブルなのか⁉AI半導体の覇権は日本！日本株はもう下がらない！【TOPIX／オルカン／S＆P500／NASDAQ100／FANG+】.md"
)


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.replace("**", "").replace("__", "").replace("*", "")
    return text.strip()


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    output = source.with_name(f"{source.stem}_Googleドキュメント用.docx")

    document = Document()
    normal_style = document.styles["Normal"]
    normal_style.font.name = "Yu Gothic"
    normal_style.font.size = Pt(11)

    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        # Original manuscript page-number markers such as "    10|".
        if re.fullmatch(r"\s*\d+\|\s*", line) or line == "---":
            continue

        if not line.strip():
            continue

        heading = re.fullmatch(r"(#{1,6})\s+(.+)", line)
        if heading:
            level = min(len(heading.group(1)), 3)
            text = clean_inline(heading.group(2))
            if level == 1:
                document.add_heading(text, 0)
            else:
                document.add_heading(text, level - 1)
            continue

        quote = re.fullmatch(r">\s?(.*)", line)
        if quote:
            text = clean_inline(quote.group(1))
            if text:
                document.add_paragraph(text, style="Quote")
            continue

        bullet = re.fullmatch(r"\s*[-*]\s+(.+)", line)
        if bullet:
            document.add_paragraph(clean_inline(bullet.group(1)), style="List Bullet")
            continue

        ordered = re.fullmatch(r"\s*\d+[.)]\s+(.+)", line)
        if ordered:
            document.add_paragraph(clean_inline(ordered.group(1)), style="List Number")
            continue

        paragraph = document.add_paragraph()
        paragraph.add_run(clean_inline(line))

    section = document.sections[0]
    footer = section.footer.paragraphs[0]
    footer.add_run("Googleドキュメントへアップロードして編集できます。")
    footer.add_run().add_break(WD_BREAK.LINE)
    footer.add_run(f"作成元: {source.name}")

    document.save(output)
    print("Created Google Docs DOCX")


if __name__ == "__main__":
    main()
