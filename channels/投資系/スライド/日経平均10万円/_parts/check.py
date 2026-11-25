# -*- coding: utf-8 -*-
"""
レイアウトの崩れを、PDFの実レンダリングから機械的に拾う。

    python check.py            … 全ページを検査して、怪しいページだけ出す
    python check.py 12 34      … そのページだけ詳しく出す

見ているもの
  1. はみ出し   … 文字がスライドの外、または端にかかっている
  2. ヘッダー被り … 文字が上部の帯（高さ53px）に食い込んでいる
  3. フッター被り … 文字が下端の帯に食い込んでいる
  4. 重なり     … 文字のブロック同士が重なっている
  5. スカスカ   … 中身が上半分で終わり、下が大きく空いている
"""
import os, sys, io, fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "..", "日経平均10万円.pdf")

W, H = 1280.0, 720.0
HDR = 53.0          # ヘッダー帯（上5pxの線＋48pxの帯）
EDGE = 10.0         # 端の余白。これより外は「はみ出し」
SPARSE_Y = 0.60     # 中身の下端がここより上なら「スカスカ」候補
SPARSE_GAP = 170.0  # かつ、下の空きがこれ以上あれば報告


def boxes(page, sx, sy):
    """文字のあるブロックを、1280x720 に正規化して返す"""
    out = []
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, txt = b[0] * sx, b[1] * sy, b[2] * sx, b[3] * sy, b[4]
        t = txt.strip()
        if t:
            out.append((x0, y0, x1, y1, t.replace("\n", " ")))
    return out


def overlap(a, b):
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    return ox, oy


def main():
    doc = fitz.open(PDF)
    want = [int(a) for a in sys.argv[1:]] or None
    bad = {}

    for i, page in enumerate(doc, 1):
        if want and i not in want:
            continue
        r = page.rect
        sx, sy = W / r.width, H / r.height
        bs = boxes(page, sx, sy)
        if not bs:
            continue
        issues = []

        # 1. はみ出し
        for b in bs:
            if b[0] < EDGE or b[2] > W - EDGE or b[1] < 0 or b[3] > H:
                issues.append("はみ出し: 「%s」 x=%.0f〜%.0f y=%.0f〜%.0f"
                              % (b[4][:26], b[0], b[2], b[1], b[3]))

        # 2. ヘッダー帯への食い込み（帯そのものの文字＝左上のラベルは除く）
        for b in bs:
            if b[1] < HDR and b[0] > 120:
                issues.append("ヘッダー被り: 「%s」 y=%.0f" % (b[4][:26], b[1]))

        # 3. 下端からはみ出し
        for b in bs:
            if b[3] > H - 4:
                issues.append("下端: 「%s」 y末=%.0f" % (b[4][:26], b[3]))

        # 4. ブロック同士の重なり（8px以上重なったら報告）
        for j in range(len(bs)):
            for k in range(j + 1, len(bs)):
                ox, oy = overlap(bs[j], bs[k])
                if ox > 8 and oy > 8:
                    issues.append("重なり: 「%s」×「%s」 %.0f×%.0f"
                                  % (bs[j][4][:16], bs[k][4][:16], ox, oy))

        # 5. スカスカ（下が大きく空いている）
        # ※ t-section（セクション扉）は、番号と見出しを左上に置く既定レイアウトで
        #    下が空くのが正しい。除外する（PART n / 13 の有無で判定）
        is_divider = any("PART" in b[4] and "/" in b[4] for b in bs)
        low = max(b[3] for b in bs)
        if is_divider:
            low = H
        if low < H * SPARSE_Y and (H - low) > SPARSE_GAP:
            issues.append("スカスカ: 中身の下端 y=%.0f（下に%.0fpx空き）" % (low, H - low))

        if issues:
            bad[i] = issues

    if want:
        for i in want:
            print("── %d ページ" % i)
            for s in bad.get(i, ["（問題なし）"]):
                print("   ", s)
        return

    print("検査 %d ページ中、%d ページに指摘" % (doc.page_count, len(bad)))
    kinds = {}
    for i, iss in bad.items():
        for s in iss:
            kinds[s.split(":")[0]] = kinds.get(s.split(":")[0], 0) + 1
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        print("   %s … %d件" % (k, v))
    print()
    for i in sorted(bad):
        print("p%03d" % i)
        for s in bad[i][:4]:
            print("     ", s)


if __name__ == "__main__":
    main()
