# ベースイメージを指定
FROM python:3.11

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコピー
COPY . /app

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリを起動
CMD ["flask", "run", "--host=0.0.0.0"]
