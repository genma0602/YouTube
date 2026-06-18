# -*- coding: utf-8 -*-
"""
スライド変換スクリプト (HTML → PDF → PNG)

使い方:
    python convert.py "日経平均7万円突破.html"
    （引数を省略するとフォルダ内の最初の .html を変換）

出力:
    <name>.pdf            … 横送りで見られる1ファイル（どのPCでも開ける）
    PNG/slide_01.png …    … 1枚ずつのPNG(1920x1080)。動画編集のタイムライン用

必要:
    - Google Chrome または Microsoft Edge
    - Python パッケージ PyMuPDF  →  pip install pymupdf
"""
import os, sys, glob, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def find_browser():
    pf  = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    candidates = [
        os.path.join(pf,   r"Google\Chrome\Application\chrome.exe"),
        os.path.join(pf86, r"Google\Chrome\Application\chrome.exe"),
        os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe"),
        os.path.join(pf,   r"Microsoft\Edge\Application\msedge.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    sys.exit("ChromeもEdgeも見つかりません。")

def main():
    os.chdir(HERE)
    html = sys.argv[1] if len(sys.argv) > 1 else None
    if not html:
        htmls = glob.glob("*.html")
        if not htmls:
            sys.exit("HTMLが見つかりません。")
        html = htmls[0]
    if not os.path.exists(html):
        sys.exit(f"HTMLが見つかりません: {html}")

    base = os.path.splitext(os.path.basename(html))[0]
    pdf  = os.path.join(HERE, base + ".pdf")
    tmp  = os.path.join(HERE, "_out_tmp.pdf")

    browser = find_browser()
    print(f"PDF生成中... ({os.path.basename(browser)})")
    subprocess.run([
        browser, "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--print-to-pdf={tmp}", "--no-pdf-header-footer",
        os.path.join(HERE, html),
    ], check=False)
    if not os.path.exists(tmp):
        sys.exit("PDF生成に失敗しました。")
    shutil.move(tmp, pdf)
    print("→", pdf)

    try:
        import fitz
    except ImportError:
        sys.exit("PyMuPDF が未インストールです。 pip install pymupdf を実行してください。")

    print("PNG書き出し中...")
    doc = fitz.open(pdf)
    out = os.path.join(HERE, "PNG")
    os.makedirs(out, exist_ok=True)
    mat = fitz.Matrix(2, 2)   # 960x540pt × 2 = 1920x1080px
    for i, page in enumerate(doc, 1):
        page.get_pixmap(matrix=mat).save(os.path.join(out, f"slide_{i:02d}.png"))
    print(f"PNG {doc.page_count} 枚 → {out}")
    print("完了")

if __name__ == "__main__":
    main()
