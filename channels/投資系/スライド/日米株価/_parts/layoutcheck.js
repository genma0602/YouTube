// スライドのレイアウト点検: node layoutcheck.js <html> <out.json>
const puppeteer = require("puppeteer-core");
const fs = require("fs");
const path = require("path");
(async () => {
  const [, , html, out] = process.argv;
  const browser = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new" });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });
  await page.goto("file:///" + path.resolve(html).replace(/\\/g, "/"), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const res = await page.evaluate(() => {
    const issues = [];
    const slides = [...document.querySelectorAll("section.slide")];
    const lines = (el) => {
      const r = document.createRange(); r.selectNodeContents(el);
      const rects = [...r.getClientRects()].filter((x) => x.width > 2);
      const fs = parseFloat(getComputedStyle(el).fontSize);
      const bots = rects.map((x) => x.bottom).sort((a, b) => a - b);
      let n = 0, last = -1e9;
      for (const y of bots) { if (y > last + fs * 0.7) { n++; last = y; } }
      return n;
    };
    const brs = (el) => el.querySelectorAll("br").length;
    slides.forEach((s, i) => {
      const n = i + 1;
      const sr = s.getBoundingClientRect();
      const hdr = s.querySelector(".hdr");
      const hdrBottom = hdr ? hdr.getBoundingClientRect().bottom - sr.top : 0;
      const foot = s.querySelector(".foot-bar");
      const footTop = foot ? foot.getBoundingClientRect().top - sr.top : 720;
      const fnote = s.querySelector(".foot-note");
      const fnoteTop = fnote ? fnote.getBoundingClientRect().top - sr.top : 720;
      const cls = s.className.replace("slide ", "");
      const add = (kind, el, extra) => issues.push({ n, cls, kind, text: (el ? el.textContent : "").trim().replace(/\s+/g, " ").slice(0, 40), extra });
      // 1) 枠外・ヘッダー/フッターとの重なり
      s.querySelectorAll("*").forEach((el) => {
        if (el.closest(".hdr") || el.closest(".foot-bar") || el.closest(".foot-note")) return;
        if (el.classList.contains("foot-bar") || el.classList.contains("hdr") || el.classList.contains("foot-note")) return;
        if (!el.children.length && !el.textContent.trim()) return;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        const t = r.top - sr.top, b = r.bottom - sr.top, l = r.left - sr.left, rt = r.right - sr.left;
        const leaf = ![...el.children].some((c) => c.textContent.trim());
        if (!leaf) return;
        if (rt > 1282 || l < -2 || b > 722) add("枠外", el, `l${l|0} r${rt|0} b${b|0}`);
        if (hdr && t < hdrBottom - 2 && !s.classList.contains("t-title") && !s.classList.contains("t-closing")) add("ヘッダーと重なる", el, `top${t|0}`);
        if (foot && b > footTop + 2) add("フッター帯と重なる", el, `b${b|0} foot${footTop|0}`);
        if (fnote && b > fnoteTop + 2 && !el.closest(".foot-note")) add("下の注記と重なる", el, `b${b|0} note${fnoteTop|0}`);
        // 横にはみ出す（nowrap 等）
        if (el.scrollWidth > el.clientWidth + 3 && getComputedStyle(el).overflow !== "visible") add("横はみ出し", el, `${el.scrollWidth}>${el.clientWidth}`);
        // 小さすぎる文字
        const fs = parseFloat(getComputedStyle(el).fontSize);
        if (fs < 18 && el.textContent.trim().length > 6) add("文字が小さい", el, `${fs}px`);
      });
      // 2) 折り返しの点検（意図した<br>より行が多い）
      const chk = (sel, kind, slack = 0) => s.querySelectorAll(sel).forEach((el) => {
        const L = lines(el), want = brs(el) + 1 + slack;
        if (L > want) add(kind, el, `${L}行（想定${want}）`);
      });
      chk(".h-main", "見出しが折り返し");
      chk(".mfig", "大きな数字が折り返し");
      chk(".val2", "表の数字が折り返し");
      chk(".t-steps .v", "階段の数字が折り返し");
      chk(".t-vs .big", "VSの文字が折り返し");
      chk(".node", "フローの箱が折り返し");
      chk(".ctitle", "カード見出しが折り返し");
      chk(".stmt", "本文が折り返し");
      chk(".cond3 .t", "ボードの文字が折り返し");
      chk(".cond3 .c", "ボードの一言が折り返し");
      chk(".t-rank .nm, .t-rank .pct", "ランキングが折り返し");
      chk(".release", "結論帯が折り返し");
      chk(".foot-bar", "フッター帯が折り返し");
      chk(".t-vs .name, .t-vs .cap", "VSの小見出しが折り返し");
      chk(".mlbl", "数字のラベルが折り返し");
      chk(".lead", "リードが折り返し");
      chk(".t-stats .nm, .t-stats .lbl, .t-stats .cd", "表のラベルが折り返し");
      // 2b) 1行固定の文字が、入れ物の内側からはみ出していないか
      s.querySelectorAll(".mfig, .val2, .t-steps .v, .c-v, .r-v, .mk .val, .pct, .pval").forEach((el) => {
        const box = el.closest(".metric, .col, .step, .card, .result, .row, .track, .mk") || el.parentElement;
        const br = box.getBoundingClientRect(), r = el.getBoundingClientRect();
        const range = document.createRange(); range.selectNodeContents(el);
        const tr = range.getBoundingClientRect();
        if (tr.right > br.right + 1 || tr.left < br.left - 1) add("入れ物からはみ出し", el, `text ${tr.left|0}-${tr.right|0} box ${br.left|0}-${br.right|0}`);
        if (tr.right > sr.right - 8 || tr.left < sr.left + 8) add("画面の端に近すぎ", el, `${tr.left|0}-${tr.right|0}`);
      });
      // 3) 数直線のラベル重なり
      const vals = [...s.querySelectorAll(".mk .val, .mk .lab")].map((e) => e.getBoundingClientRect());
      for (let a = 0; a < vals.length; a++) for (let b = a + 1; b < vals.length; b++) {
        const A = vals[a], B = vals[b];
        if (A.left < B.right && B.left < A.right && A.top < B.bottom && B.top < A.bottom) add("数直線のラベルが重なる", null, "");
      }
      // 4) 余白過多：中身の下端が上半分で終わる
      const content = [...s.children].filter((c) => !c.classList.contains("hdr") && !c.classList.contains("foot-bar") && !c.classList.contains("foot-note"));
      if (content.length) {
        const top = Math.min(...content.map((c) => c.getBoundingClientRect().top)) - sr.top;
        const bot = Math.max(...content.map((c) => c.getBoundingClientRect().bottom)) - sr.top;
        const free = 720 - (foot ? 720 - footTop : 0);
        if (bot < free * 0.62 && !s.classList.contains("t-title")) add("下が空きすぎ", null, `中身 ${top|0}〜${bot|0}`);
      }
    });
    return issues;
  });
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  console.log("issues", res.length);
  await browser.close();
})();
