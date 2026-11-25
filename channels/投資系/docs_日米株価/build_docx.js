// 本文のみ.md → Googleドキュメント用 .docx（いつもの形）
// 行間と段落の間隔は TOPIX改革の docx と同じ：本文は段落後10pt・行間1.15、見出し1は前24pt、見出し2は前10pt、題名は後15pt
// 使い方: node build_docx.js <input.md> <output.docx>   （docx パッケージが要る。無ければ npm install docx）
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require("docx");

const [, , inPath, outPath] = process.argv;
const lines = fs.readFileSync(inPath, "utf8").split(/\r?\n/);

const BODY = { after: 200, line: 276 };          // 10pt 後ろ・1.15行
const children = [];
for (const raw of lines) {
  const line = raw.trimEnd();
  if (line.trim() === "") continue;
  if (line.startsWith("# ")) {
    children.push(new Paragraph({ heading: HeadingLevel.TITLE, spacing: { after: 300, line: 240 }, children: [new TextRun(line.slice(2))] }));
  } else if (line.startsWith("## ")) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 480, after: 0, line: 276 }, keepNext: true, children: [new TextRun(line.slice(3))] }));
  } else if (line.startsWith("### ")) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 0, line: 276 }, keepNext: true, children: [new TextRun(line.slice(4))] }));
  } else {
    children.push(new Paragraph({ spacing: BODY, children: [new TextRun(line)] }));
  }
}

const doc = new Document({
  styles: {
    default: {
      document: { run: { size: 22 }, paragraph: { spacing: BODY } },
      title: { run: { size: 52, bold: true }, paragraph: { spacing: { after: 300, line: 240 } } },
      heading1: { run: { size: 28, bold: true }, paragraph: { spacing: { before: 480, after: 0 }, keepNext: true } },
      heading2: { run: { size: 26, bold: true }, paragraph: { spacing: { before: 200, after: 0 }, keepNext: true } },
    },
  },
  sections: [{ children }],
});
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log("written", outPath, buf.length, "bytes,", children.length, "paragraphs");
});
