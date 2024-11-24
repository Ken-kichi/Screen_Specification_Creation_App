import os
from flask import request
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# 画面設計書クラス


class Screen_design_document:
    # 初期値設定
    def __init__(self, file, static_folder):
        self.file = file
        self.static_folder = static_folder

    # 画像アップロード関数
    def upload_file(self):
        try:
            file_path = os.path.join(
                self.static_folder, self.file.filename)
            self.file.save(file_path)
        except Exception as e:
            print(f"ファイルの保存中にエラーが発生しました: {e}")

    # OpenAI接続関数
    def connect_openai(self, file, model, max_tokens, csv_items):

        uploaded_url = request.host_url + "uploads/" + file.filename

        openai_response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"あなたは一流のエンジニア兼コンサルタントです。画像を解析してCSV形式のみで出力してください。項目は以下のようにしてください。{csv_items}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                    "url": uploaded_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )

        return openai_response

    # csv出力関数
    def get_generate_csv(self, file, model, max_tokens, csv_items):
        response = self.connect_openai(
            file,
            model,
            max_tokens,
            csv_items
        )

        generated_csv = ""
        response_content = response.choices[0].message.content
        split_text = response_content.split("```")
        for text in split_text:
            if text.split("\n")[0] == "csv":
                generated_csv = text[4:]
                break

        if generated_csv == "":
            return response_content
        return generated_csv
