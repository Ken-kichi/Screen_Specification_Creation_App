import os
from flask import Flask, request, render_template, send_from_directory
from openai import OpenAI
from Screen_design_document import Screen_design_document

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

            csv_data = screen_design.get_generate_csv(file)

            # 部分HTMLを返す
        return render_template("index.html", specification=csv_data)
    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    # if not uploads folder,create it.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
