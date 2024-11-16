import os
from flask import Flask, request, render_template, send_from_directory, render_template_string
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


class screen_design_document:
    def __init__(self, file, static_folder):
        self.file = file
        self.static_folder = static_folder

    def upload_file(self, file):
        try:
            file_path = os.path.join(
                self.static_folder, file.filename)
            file.save(file_path)
        except Exception as e:
            print(f"ファイルの保存中にエラーが発生しました: {e}")

    def connect_openai(self, file):

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
                                    # "url": request.host_url + "uploads/" + file.filename,
                                    "url": "https://mkasumi.com/archives/001/201506/8cd040908b1da6f9a7a4a1f482b32acd.jpg",
                                },
                            },
                    ],
                }
            ],
            max_tokens=300,
        )

    def get_generate_csv(self, file):
        response = self.connect_openai(file)

        generated_csv = ""
        split_text = response.choices[0].message.content.split("```")
        for text in split_text:
            if text.split("\n")[0] == "csv":
                generated_csv = text[4:]
        return generated_csv

    def create_response_message(self, csv_text):
        if csv_text == "":
            return render_template_string(
                """
                        <h2>画面設計書の生成に失敗しました。</h2>
                        """
            )

        table_rows = []
        for line in csv_text.strip().split("\n"):
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
