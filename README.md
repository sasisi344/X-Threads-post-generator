# Blog to SNS Post Generator

ブログ記事のURLを入力するだけで、X（旧Twitter）とThreadsに最適化された投稿文案を自動生成するWebアプリケーションです。
Google Gemini 2.0 Flash と Jina Reader API を活用し、記事の内容を深く理解した魅力的なポストを作成します。

## ✨ 特徴

- **自動生成**: ブログURLを入力するだけで、X用（140字以内、箇条書き）とThreads用（ストーリー重視）の2つの投稿案を生成。
- **ペルソナ選択**: 投稿の文体（スタイル）を5つのタイプから選択可能。
    - 🌟 インフルエンサー
    - 📊 マーケティング（CMO）
    - ✍️ ブロガー
    - 👤 一般人
    - 🔧 ギーク（熱量高めのテック愛好家）
- **言語自動判定**: 記事の言語に合わせて、出力言語を自動で調整（日本語記事なら日本語で生成）。
- **Docker対応**: Dockerで簡単に環境構築が可能。

## 🛠 技術スタック

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.0 Flash (via `google-generativeai`)
- **Scraper**: Jina Reader API
- **Infrastructure**: Docker / Docker Compose

## 🚀 セットアップ

### 前提条件

- [Google AI Studio](https://aistudio.google.com/) でAPIキーを取得していること。

### 1. プロジェクトのクローン

```bash
git clone <repository-url>
cd thread-x-post
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、APIキーを設定します。

```bash
# Windows (PowerShell)
Copy-Item ".env.example" ".env"
```

`.env` ファイルを開き、`GEMINI_API_KEY` に取得したキーを入力してください。

```text
GEMINI_API_KEY=your_api_key_here
```

### 3. アプリケーションの起動

#### Dockerを使用する場合（推奨）

```bash
docker compose up --build
```

起動後、ブラウザで `http://localhost:8501` にアクセスしてください。

#### ローカルで実行する場合

Python 3.9以上が必要です。

```bash
# 依存関係のインストール
pip install -r requirements.txt

# アプリの実行
python -m streamlit run app.py
```

## 📖 使い方

1. アプリケーションを開く。
2. サイドバーでAPIキーが設定されていることを確認する（✅ API Key: 設定済み）。
3. **「投稿スタイルを選択」** ドロップダウンから、希望する文体（ペルソナ）を選ぶ。
4. **「Blog URL」** フォームに記事のURLを入力する。
5. **「投稿を作成する」** ボタンをクリック。
6. 生成されたX用とThreads用のポストを確認・コピーする。

## 📄 License

MIT License
