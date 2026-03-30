from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")

    sentences = text.split(".")

    if len(sentences) > 2:
        summary = ". ".join(sentences[:2]) + "."
    else:
        summary = text

    return jsonify({"result": "Summary: " + summary})

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    text = ""

    if file.filename.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    else:
        text = file.read().decode("utf-8")

    return jsonify({"result": "Summary: " + text[:200]})