import os
from flask import Flask, request, render_template, send_from_directory
from openai import OpenAI
from Screen_design_document import Screen_design_document
import json

# Set API Key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        # file upload
        file = request.files["file"]

        screen_design = Screen_design_document(
            file, app.config['UPLOAD_FOLDER']
        )

        screen_design.upload_file()

        if file and file.filename.endswith((".png", ".jpg", ".jpeg")):

            model = "gpt-4o-mini"
            max_tokens = 1000
            json_items = "No.,項目名,項目ID,入力形式,必須,エラーメッセージ,表示順,ラベル名,プレースホルダー,最大文字数,最小文字数,説明文"

            attempt = 0
            max_attempt = 2
            csv_data = None

            #二回を上限に生成データが取れるまで通信を繰り返す
            while max_attempt >= attempt:
                try:
                    json_data = screen_design.get_generate_json(
                        file,
                        model,
                        max_tokens,
                        json_items
                    )
                    dict_data = json.loads(json_data)
                    headers = dict_data["formItems"][0].keys()
                    if (headers):
                        csv_data = ",".join(headers) + "\n"
                        for item in dict_data["formItems"]:
                            for value in item.values():
                                csv_data += str(value) + ","
                            csv_data = csv_data[:-1] + "\n"
                        break
                except Exception as e:
                    attempt += 1
                    print(f"エラーが発生：{e}")

            if (csv_data):
                return render_template("index.html", specification_header=headers, specification=dict_data["formItems"], csv_data=csv_data)
            else:
                return render_template("index.html", message="エラーが発生しました。")

    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    # if not uploads folder,create it.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
