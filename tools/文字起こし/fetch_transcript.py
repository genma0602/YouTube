#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube動画の文字起こしを取得するツール
URL または 動画ID を渡すと、字幕（手動・自動生成どちらも）を取得して表示・保存します。

使用ライブラリ: https://github.com/jdepoix/youtube-transcript-api
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("エラー: youtube-transcript-api がインストールされていません。", file=sys.stderr)
    print("  pip install youtube-transcript-api", file=sys.stderr)
    sys.exit(1)

try:
    from youtube_transcript_api.exceptions import (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
    )
except ImportError:
    from youtube_transcript_api._errors import (  # type: ignore
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
    )


def extract_video_id(url_or_id: str) -> str | None:
    """YouTubeのURLまたは動画IDから video_id を抽出する"""
    s = (url_or_id or "").strip()
    if not s:
        return None
    # 動画IDのみ（11文字の英数字とハイフン・アンダースコア）
    if re.match(r"^[\w-]{11}$", s):
        return s
    # https://www.youtube.com/watch?v=VIDEO_ID
    m = re.search(r"[?&]v=([\w-]{11})", s)
    if m:
        return m.group(1)
    # https://youtu.be/VIDEO_ID
    m = re.search(r"youtu\.be/([\w-]{11})", s)
    if m:
        return m.group(1)
    # ショート: https://www.youtube.com/shorts/VIDEO_ID
    m = re.search(r"/shorts/([\w-]{11})", s)
    if m:
        return m.group(1)
    return None


def run(
    url_or_id: str,
    *,
    languages: list[str] | None = None,
    output_path: str | None = None,
) -> str:
    """
    文字起こしを取得して1つのテキストにまとめる。
    戻り値: 全文テキスト
    """
    video_id = extract_video_id(url_or_id)
    if not video_id:
        raise ValueError(f"YouTubeのURLまたは動画IDを指定してください: {url_or_id}")

    if languages is None:
        languages = ["ja", "en"]  # 日本語優先、なければ英語

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=languages)
    except NoTranscriptFound:
        raise ValueError(
            f"動画 {video_id} には指定した言語の字幕がありません。"
            " 手動・自動字幕がオフの動画は取得できません。"
        )
    except TranscriptsDisabled:
        raise ValueError(f"動画 {video_id} では字幕が無効です。")
    except VideoUnavailable:
        raise ValueError(f"動画 {video_id} は存在しないか、非公開・削除されています。")

    lines: list[str] = []
    for snippet in transcript:
        text = (snippet.text or "").strip()
        if not text:
            continue
        lines.append(text)

    full_text = "\n".join(lines)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(full_text, encoding="utf-8")

    return full_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="YouTube動画の文字起こしを取得する（URL or 動画ID）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python fetch_transcript.py "https://www.youtube.com/watch?v=xxxxx"
  python fetch_transcript.py xxxxx -o 書き起こし.txt
  python fetch_transcript.py xxxxx --languages ja en
        """,
    )
    parser.add_argument(
        "url_or_id",
        help="YouTubeのURL または 動画ID（11文字）",
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_path",
        metavar="FILE",
        help="書き起こしを保存するファイルパス",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["ja", "en"],
        metavar="LANG",
        help="取得する言語の優先順（例: ja en）。デフォルト: ja en",
    )
    args = parser.parse_args()

    try:
        text = run(
            args.url_or_id,
            languages=args.languages,
            output_path=args.output_path,
        )
        if not args.output_path:
            print(text)
        else:
            print(f"保存しました: {args.output_path}", file=sys.stderr)
    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
