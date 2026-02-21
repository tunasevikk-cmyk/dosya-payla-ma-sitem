from flask import Flask, render_template, request, send_from_directory
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file or file.filename == "":
        return "Dosya seçilmedi"

    file_id = str(uuid.uuid4())[:8]
    folder_path = os.path.join(UPLOAD_FOLDER, file_id)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, file.filename)
    file.save(file_path)

    download_link = request.host_url + "file/" + file_id
    return f"Paylaşım linki: <a href='{download_link}'>{download_link}</a>"

@app.route("/file/<file_id>")
def get_file(file_id):
    folder_path = os.path.join(UPLOAD_FOLDER, file_id)

    if not os.path.exists(folder_path):
        return "Dosya bulunamadı"

    files = os.listdir(folder_path)
    if not files:
        return "Dosya bulunamadı"

    return send_from_directory(folder_path, files[0], as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
