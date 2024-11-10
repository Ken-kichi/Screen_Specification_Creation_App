# 画面仕様書作成アプリ

このアプリは、アップロードされた画像を解析し、画面設計書を生成するためのFlaskベースのウェブアプリケーションです。OpenAIのAPIを使用して、画像に基づいた設計書を作成します。

## 機能

- 画像ファイル（PNG、JPG、JPEG）のアップロード
- アップロードされた画像を解析し、設計書を生成
- 生成された設計書をウェブページに表示

## 必要な環境

- Python 3.x
- Flask
- OpenAI
- Pillow
- python-dotenv
- supabase-py

## インストール手順

1. リポジトリをクローンします。
   ```bash
   git clone <リポジトリのURL>
   cd <リポジトリ名>
   ```

2. 必要なパッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```

3. `.env`ファイルを作成し、以下の環境変数を設定します。
   ```
   OPENAI_KEY=<あなたのOpenAI APIキー>
   SUPABASE_URL=<あなたのSupabaseのURL>
   SUPABASE_ANON_KEY=<あなたのSupabaseの匿名キー>
   ```

4. アプリを実行します。
   ```bash
   python app.py
   ```

5. ブラウザで `http://127.0.0.1:5000` にアクセスします。

## 使用方法

1. アップロードフォームに画像ファイルを選択します。
2. 「upload」ボタンをクリックします。
3. 解析された画面設計書が表示されます。

## 注意事項

- アップロードできる画像の形式はPNG、JPG、JPEGのみです。
- OpenAIのAPIキーが必要です。APIキーがない場合は、OpenAIの公式サイトから取得してください。

## ライセンス
このプロジェクトはMITライセンスの下で提供されています。
