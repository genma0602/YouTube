# 01_YouTube — アーカイブ

> **このワークスペースは旧構造です。**
> チャンネルごとに独立ワークスペースへ移行しました。

## 移行先

| チャンネル | 場所 |
|-----------|------|
| 忍び経済学 | `C:\Users\genki\忍び経済学\` |

## 新チャンネルを作る場合

`channels/_template/` を丸ごとコピーして、新しいフォルダ名にリネームし、独立ワークスペースとして開く。

## このフォルダに残っているもの

| Folder | 内容 |
|--------|------|
| channels/_template | 新構造のテンプレート |
| channels/忍び経済学 | 移行済み（コピー元・削除可能） |
| docs | Cursor/ClaudeCode セットアップ手順（チャンネル非依存） |
| data1 | 関西企業リスト（YouTube無関係） |
| tools | 文字起こしスクリプト（忍び経済学に移行済み） |

## 別PCで同じように使う手順

### 1) リポジトリを取得

```powershell
git clone https://github.com/genma0602/YouTube.git
cd YouTube
```

### 2) Python環境を作成（任意だが推奨）

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3) 必要ライブラリをインストール

```powershell
pip install -r requirements.txt
```

### 4) スクリプト実行

```powershell
python .\generate_kansai_companies.py
```

生成ファイルは `data1/関西_主要企業リスト.xlsx` に保存されます。  
（出力先はスクリプト相対パスにしてあるので、PC固有の絶対パスに依存しません）
