import os
from flask import Flask, request, render_template, send_from_directory, render_template_string
from openai import OpenAI
from io import StringIO

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


class Screen_design_document:
    def __init__(self, file, static_folder):
        self.file = file
        self.static_folder = static_folder

    def upload_file(self):
        try:
            file_path = os.path.join(
                self.static_folder, self.file.filename)
            self.file.save(file_path)
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
                             "text": "あなたは一流のエンジニア兼コンサルタントです。画像を解析してCSV形式のみで出力してください。項目は以下のようにしてください。No.,項目名,項目ID,入力形式,必須,バリデーション,エラーメッセージ,表示順,ラベル名,プレースホルダー,最大文字数,最小文字数,説明文"
                             },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": request.host_url + "uploads/" + file.filename,
                                },
                            },
                    ],
                }
            ],
            # 開発時には出力トークンを制御して結果を確認する
            max_tokens=1000,
        )

    def get_generate_csv(self, file):
        response = self.connect_openai(file)

        generated_csv = ""
        isResult = False

        while isResult == False:
            split_text = response.choices[0].message.content.split("```")
            for text in split_text:
                if text.split("\n")[0] == "csv":
                    generated_csv = text[4:]
            if generated_csv != "":
                isResult = True
                break

        return generated_csv
