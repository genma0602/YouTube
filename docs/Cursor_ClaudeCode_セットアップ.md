# Cursor で Claude Code を使うためのセットアップ

## 実施済みの設定（2025年2月）

### 1. Claude Code CLI のインストール
- **場所**: `C:\Users\genki\.local\bin\claude.exe`
- **バージョン**: 2.1.56
- **PATH**: ユーザー環境変数に `%USERPROFILE%\.local\bin` を追加済み

### 2. Cursor 拡張機能
- **拡張**: Claude Code (anthropic.claude-code) v2.1.56
- マーケットプレイスからインストール済み

---

## 初回だけやっておくこと

### 1. ターミナルを開き直す
PATH を反映するため、**Cursor を一度終了して開き直す**か、新しいターミナルを開いてください。

### 2. Claude にログインする
- Claude Code は **Pro / Max / Teams / Enterprise / Console** のいずれかのアカウントが必要です（無料の claude.ai のみでは利用できません）。
- Cursor で **拡張機能の「Claude Code」** を開き、表示される手順でブラウザからログインしてください。
- またはターミナルで `claude` を実行し、表示されるリンクからログインしても構いません。

---

## Cursor での使い方

1. **Claude Code パネルを開く**
   - エディタ右上の **Spark アイコン（✨）** をクリック
   - または **Ctrl+Shift+P** → 「Claude Code」で検索 → 「Open in New Tab」など

2. **ステータスバー**
   - 画面右下の **「✱ Claude Code」** をクリックしても開けます。

3. **ショートカット**
   - **Alt+K**: 選択範囲を @ メンションとしてプロンプトに挿入

---

## トラブルシューティング

- **「claude が見つかりません」**
  - Cursor を再起動し、新しいターミナルで `claude --version` を実行して PATH を確認してください。
  - まだダメな場合は、Windows の「環境変数」でユーザーの PATH に `C:\Users\genki\.local\bin` が入っているか確認してください。

- **拡張が有効にならない**
  - Cursor を完全に終了してから起動し直してください。
  - 拡張機能ビュー（Ctrl+Shift+X）で「Claude Code」が有効になっているか確認してください。

- **Git for Windows**
  - Claude Code は Windows で **Git for Windows** を前提にしています。未導入の場合は [Git for Windows](https://git-scm.com/download/win) をインストールしてください。
