# scenario_draft.md -> preview.html (読み上げ本文と編集メモを分離した閲覧用ページ)
$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'scenario_draft.md'
$out = Join-Path $PSScriptRoot 'preview.html'
$lines = Get-Content $src -Encoding utf8

function Esc([string]$s) {
  $s = $s -replace '&','&amp;' -replace '<','&lt;' -replace '>','&gt;'
  $s = [regex]::Replace($s, '\[([^\]]*)\]\([^)]*\)', '$1')
  $s = [regex]::Replace($s, '\*\*(.+?)\*\*', '<strong>$1</strong>')
  return $s
}

$title = ''
$sections = New-Object System.Collections.ArrayList
$cur = $null
$pendingNote = New-Object System.Collections.ArrayList

function Flush-Note {
  if ($pendingNote.Count -gt 0 -and $null -ne $cur) {
    $html = ($pendingNote | ForEach-Object { '<p>' + (Esc $_) + '</p>' }) -join ''
    [void]$cur.blocks.Add(@{ kind='note'; html=$html })
    $pendingNote.Clear()
  }
}

function New-Section([string]$heading, [int]$level) {
  return @{ heading=$heading; level=$level; blocks=(New-Object System.Collections.ArrayList); chars=0 }
}

foreach ($raw in $lines) {
  $line = $raw.TrimEnd()
  if ($line -match '^#\s+(.+)$') { $title = $Matches[1]; continue }
  if ($line -match '^##\s+(.+)$') {
    Flush-Note
    $cur = New-Section $Matches[1] 2
    [void]$sections.Add($cur); continue
  }
  if ($line -match '^###\s+(.+)$') {
    Flush-Note
    $cur = New-Section $Matches[1] 3
    [void]$sections.Add($cur); continue
  }
  if ($line -match '^---\s*$') { continue }
  if ($line -match '^\s*$') { Flush-Note; continue }
  if ($line -match '^>\s?(.*)$') {
    $t = $Matches[1].Trim()
    if ($t -ne '') { [void]$pendingNote.Add($t) }
    continue
  }
  if ($null -eq $cur) { continue }
  Flush-Note
  [void]$cur.blocks.Add(@{ kind='body'; html=(Esc $line) })
  $cur.chars += ($line -replace '\s','').Length
}
Flush-Note

$total = 0; foreach ($s in $sections) { $total += $s.chars }
$mins = [math]::Round($total / 325.0)

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('<title>AI半導体株はまだ序章｜台本プレビュー</title>')
[void]$sb.AppendLine(@'
<style>
:root{
  --paper:#F2F5F7; --surface:#FFFFFF; --ink:#171D25; --ink-soft:#525C69;
  --ink-faint:#7E8896; --accent:#8F6118; --accent-soft:#B98A34;
  --rule:#D9DFE5; --note-bg:#E9EDF1; --note-edge:#B6C0CB;
  --serif:"Yu Mincho","YuMincho","Hiragino Mincho ProN","Noto Serif JP",serif;
  --sans:"Yu Gothic UI","Yu Gothic","Hiragino Kaku Gothic ProN","Meiryo","Noto Sans JP",system-ui,sans-serif;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#11151A; --surface:#171C22; --ink:#E2E7EC; --ink-soft:#9BA5B1;
    --ink-faint:#6F7A87; --accent:#D3A253; --accent-soft:#A97F35;
    --rule:#28303A; --note-bg:#1C232B; --note-edge:#3A4551;
  }
}
:root[data-theme="dark"]{
  --paper:#11151A; --surface:#171C22; --ink:#E2E7EC; --ink-soft:#9BA5B1;
  --ink-faint:#6F7A87; --accent:#D3A253; --accent-soft:#A97F35;
  --rule:#28303A; --note-bg:#1C232B; --note-edge:#3A4551;
}
:root[data-theme="light"]{
  --paper:#F2F5F7; --surface:#FFFFFF; --ink:#171D25; --ink-soft:#525C69;
  --ink-faint:#7E8896; --accent:#8F6118; --accent-soft:#B98A34;
  --rule:#D9DFE5; --note-bg:#E9EDF1; --note-edge:#B6C0CB;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  -webkit-font-smoothing:antialiased}
.wrap{display:grid;grid-template-columns:minmax(0,1fr);gap:0;
  max-width:78rem;margin:0 auto;padding:0 1.25rem 6rem}
@media(min-width:1080px){.wrap{grid-template-columns:15rem minmax(0,1fr);gap:3.5rem;padding:0 2rem 6rem}}

/* ---- masthead ---- */
.masthead{grid-column:1/-1;padding:3.5rem 0 2rem;border-bottom:1px solid var(--rule)}
.kicker{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);font-weight:700;margin:0 0 1rem}
.masthead h1{font-family:var(--serif);font-weight:600;font-size:clamp(1.35rem,2.6vw,2rem);
  line-height:1.55;margin:0;text-wrap:balance;max-width:32em}
.stats{display:flex;flex-wrap:wrap;gap:2rem;margin-top:1.75rem}
.stat{display:flex;flex-direction:column;gap:.25rem}
.stat b{font-size:1.5rem;font-weight:600;font-variant-numeric:tabular-nums;line-height:1}
.stat span{font-size:.72rem;letter-spacing:.1em;color:var(--ink-faint)}
.toolbar{display:flex;gap:.6rem;margin-top:1.75rem;flex-wrap:wrap}
.btn{font:inherit;font-size:.8rem;padding:.5rem .95rem;border-radius:2px;cursor:pointer;
  background:transparent;border:1px solid var(--rule);color:var(--ink-soft);transition:.15s}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--paper)}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* ---- index ---- */
.index{display:none}
@media(min-width:1080px){
  .index{display:block;position:sticky;top:0;align-self:start;
    max-height:100vh;overflow-y:auto;padding:2.5rem 0}
}
.index ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.1rem}
.index a{display:flex;justify-content:space-between;gap:.6rem;align-items:baseline;
  text-decoration:none;color:var(--ink-soft);font-size:.8rem;line-height:1.5;
  padding:.42rem .5rem;border-radius:2px;border-left:2px solid transparent}
.index a:hover{color:var(--ink);background:var(--note-bg);border-left-color:var(--accent)}
.index a:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.index .sub a{padding-left:1.4rem;font-size:.74rem;color:var(--ink-faint)}
.index .n{font-variant-numeric:tabular-nums;font-size:.68rem;color:var(--ink-faint);
  flex:none;letter-spacing:.02em}

/* ---- script ---- */
.script{padding:2.5rem 0 0;min-width:0}
section{padding:2.75rem 0;border-bottom:1px solid var(--rule)}
section:last-child{border-bottom:0}
.head{display:flex;justify-content:space-between;align-items:baseline;gap:1.5rem;
  margin-bottom:1.75rem;flex-wrap:wrap}
h2{font-family:var(--serif);font-weight:600;font-size:1.45rem;line-height:1.5;
  margin:0;text-wrap:balance;max-width:26em}
h3{font-family:var(--serif);font-weight:600;font-size:1.12rem;line-height:1.6;
  margin:0;text-wrap:balance;max-width:28em;color:var(--ink)}
h3::before{content:"";display:block;width:1.6rem;height:2px;background:var(--accent);
  margin-bottom:.85rem}
.count{font-size:.72rem;color:var(--ink-faint);font-variant-numeric:tabular-nums;
  letter-spacing:.06em;flex:none;white-space:nowrap}
.body p{font-size:1.03rem;line-height:2.05;margin:0 0 1.45em;max-width:34em;
  color:var(--ink);text-align:justify;word-break:normal;line-break:strict;
  overflow-wrap:anywhere}
.note{background:var(--note-bg);border-left:2px solid var(--note-edge);
  padding:1rem 1.15rem;margin:0 0 1.6em;max-width:38em;border-radius:0 2px 2px 0}
.note::before{content:"編集メモ｜収録しない";display:block;font-size:.66rem;
  letter-spacing:.14em;color:var(--accent);font-weight:700;margin-bottom:.6rem}
.note p{font-size:.79rem;line-height:1.85;margin:0 0 .6em;color:var(--ink-soft)}
.note p:last-child{margin-bottom:0}
.note strong{color:var(--ink);font-weight:600}
body.reading .note{display:none}
@media print{.index,.toolbar,.note{display:none}body{background:#fff}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
'@)

[void]$sb.AppendLine('<div class="wrap">')
[void]$sb.AppendLine('<header class="masthead">')
[void]$sb.AppendLine('<p class="kicker">台本プレビュー / 読み上げ本文</p>')
[void]$sb.AppendLine('<h1>' + (Esc $title) + '</h1>')
[void]$sb.AppendLine('<div class="stats">')
[void]$sb.AppendLine('<div class="stat"><b>' + $total.ToString('N0') + '</b><span>読み上げ字数</span></div>')
[void]$sb.AppendLine('<div class="stat"><b>' + $mins + '</b><span>想定尺（分）</span></div>')
[void]$sb.AppendLine('<div class="stat"><b>11</b><span>ブロック</span></div>')
[void]$sb.AppendLine('</div>')
[void]$sb.AppendLine('<div class="toolbar">')
[void]$sb.AppendLine('<button class="btn" id="toggleNotes" aria-pressed="false" type="button">編集メモを隠す</button>')
[void]$sb.AppendLine('</div>')
[void]$sb.AppendLine('</header>')

# index
[void]$sb.AppendLine('<nav class="index" aria-label="目次"><ol>')
$i = 0
foreach ($s in $sections) {
  $i++
  $cls = if ($s.level -eq 3) { ' class="sub"' } else { '' }
  [void]$sb.AppendLine('<li' + $cls + '><a href="#s' + $i + '"><span>' + (Esc $s.heading) + '</span><span class="n">' + $s.chars.ToString('N0') + '</span></a></li>')
}
[void]$sb.AppendLine('</ol></nav>')

# body
[void]$sb.AppendLine('<main class="script">')
$i = 0
foreach ($s in $sections) {
  $i++
  [void]$sb.AppendLine('<section id="s' + $i + '">')
  $tag = if ($s.level -eq 3) { 'h3' } else { 'h2' }
  [void]$sb.AppendLine('<div class="head"><' + $tag + '>' + (Esc $s.heading) + '</' + $tag + '><span class="count">' + $s.chars.ToString('N0') + ' 字</span></div>')
  [void]$sb.AppendLine('<div class="body">')
  foreach ($b in $s.blocks) {
    if ($b.kind -eq 'body') { [void]$sb.AppendLine('<p>' + $b.html + '</p>') }
    else { [void]$sb.AppendLine('<aside class="note">' + $b.html + '</aside>') }
  }
  [void]$sb.AppendLine('</div></section>')
}
[void]$sb.AppendLine('</main></div>')

[void]$sb.AppendLine(@'
<script>
(function(){
  var b=document.getElementById('toggleNotes');
  b.addEventListener('click',function(){
    var on=document.body.classList.toggle('reading');
    b.setAttribute('aria-pressed',on?'true':'false');
    b.textContent=on?'編集メモを表示':'編集メモを隠す';
  });
})();
</script>
'@)

$sb.ToString() | Out-File -FilePath $out -Encoding utf8
Write-Output ("sections=" + $sections.Count + " total=" + $total + " mins=" + $mins)
Write-Output ("written: " + $out)
