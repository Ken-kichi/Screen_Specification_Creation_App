import os
from flask import Flask, request, render_template, send_from_directory, render_template_string
from PIL import Image
from openai import OpenAI
from dotenv import dotenv_values
from supabase import create_client, Client
import base64

config = dotenv_values(".env")
# Set API Key（ローカル環境）
# client = OpenAI(api_key=config["OPENAI_KEY"])
# Set API Key（本番環境）
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
# supabase_url = config["SUPABASE_URL"]
# supabase_anon_key = config["SUPABASE_ANON_KEY"]


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# if not uploads folder,create it.
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def upload_file(file):
    try:
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    except Exception as e:
        print(f"ファイルの保存中にエラーが発生しました: {e}")


def connect_openai(file):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                        "content": [
                            {"type": "text",
                             "text": "あなたは一流のエンジニア兼コンサルタントです。画像を解析してCSV形式のみで出力してください。項目は以下のようにしてください。No.,項目名,項目ID,入力形式,必須,バリデーション,エラーメッセージ,表示順"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": request.host_url + "uploads/" + file.filename,
                                },
                            },
                        ],
            }
        ],
        max_tokens=300,
    )


def get_generate_csv(file):
    response = connect_openai(file)

    generated_csv = ""
    split_text = response.choices[0].message.content.split("```")
    for text in split_text:
        if text.split("\n")[0] == "csv":
            generated_csv = text[4:]
    return generated_csv


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # file upload
        file = request.files["file"]
        if file and file.filename.endswith((".png", ".jpg", ".jpeg")):

            design_specification = get_generate_csv(file)

            if design_specification == "":
                return render_template_string(
                    """
                    <h2>画面設計書の生成に失敗しました。</h2>
                    """
                )

            table_rows = []
            for line in design_specification.strip().split("\n"):
                table_rows.append(line.split(","))

            # テーブルのHTMLを生成（Bootstrapスタイルを適用）
            table_html = "<table class='table table-bordered'>"
            for row in table_rows:
                table_html += "<tr>" + \
                    "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            table_html += "</table>"

            return render_template_string(
                """
                <h2>画面設計書</h2>
                {{ table_html|safe }}
                """,
                table_html=table_html
            )

    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
