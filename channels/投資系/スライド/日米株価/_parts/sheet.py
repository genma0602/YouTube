# -*- coding: utf-8 -*-
# PNG を一覧画像にまとめる: python sheet.py <開始番号> <枚数> <出力>
import sys, os, glob
from PIL import Image, ImageDraw
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PNG")
files = sorted(glob.glob(os.path.join(d, "slide_*.png")))
s, n, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
files = files[s-1:s-1+n]
W, H, C = 480, 270, 4
rows = (len(files)+C-1)//C
sheet = Image.new("RGB", (W*C, H*rows), "white")
for i, f in enumerate(files):
    im = Image.open(f).resize((W, H))
    ImageDraw.Draw(im).text((8, 8), os.path.basename(f)[6:-4], fill=(255, 0, 0))
    sheet.paste(im, ((i % C)*W, (i//C)*H))
sheet.save(out)
print(out, len(files))
