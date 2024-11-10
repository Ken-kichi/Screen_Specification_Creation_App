import os
from flask import Flask, request, render_template, send_from_directory, render_template_string
from PIL import Image
from openai import OpenAI
from dotenv import dotenv_values
from supabase import create_client, Client
import base64

config = dotenv_values(".env")
# Set API Key
client = OpenAI(api_key=config["OEPNAI_KEY"])
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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # file upload
        file = request.files["file"]
        if file and file.filename.endswith((".png", ".jpg", ".jpeg")):
            upload_file(file)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": "あなたは一流のエンジニア兼コンサルタントです。画像を解析して画面設計書を記載してください。"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    # "url": request.host_url + "uploads/" + file.filename,
                                    "url": request.host_url + "uploads/" + file.filename,
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            design_specification = response.choices[0].message

            # 部分HTMLを返す
        return render_template_string(
            """
            <h2>画面設計書</h2>
            <pre>{{ specification }}</pre>
            """,
            specification=design_specification
        )
    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
