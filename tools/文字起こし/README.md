# 文字起こしツール

全チャンネル共通で使う文字起こし用のツールです。  
**YouTubeのURLを渡すと、動画の字幕（手動・自動生成）を取得して全文を表示・保存できます。**

## セットアップ

```bash
cd tools/文字起こし
pip install -r requirements.txt
```

## 使い方

```bash
# URL を渡す（コンソールに全文表示）
python fetch_transcript.py "https://www.youtube.com/watch?v=動画ID"

# ファイルに保存
python fetch_transcript.py "https://www.youtube.com/watch?v=動画ID" -o 書き起こし.txt

# 言語を指定（日本語優先 → 英語の順）
python fetch_transcript.py "動画ID" --languages ja en
```

- **URL形式**: `https://www.youtube.com/watch?v=xxx` / `https://youtu.be/xxx` / `https://www.youtube.com/shorts/xxx` のいずれか、または **動画ID（11文字）のみ** でも可。
- APIキーは不要です（[youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) を使用）。
- 字幕がオフの動画・非公開・削除済みは取得できません。

## 書き起こし結果の保存先

- **チャンネル別に保存したい場合** → 保存先を `channels/[チャンネル名]/05_文字起こし/` にすると整理しやすいです。  
  例: `-o ../../channels/マイチャンネル/05_文字起こし/20250213_動画タイトル.txt`
