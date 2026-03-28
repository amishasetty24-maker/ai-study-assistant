from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

# 🔹 TEXT SUMMARIZATION
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text")

    print("Received:", text)

    # Simple summarization (first 2 sentences)
    sentences = text.split(".")

    if len(sentences) > 2:
        summary = ". ".join(sentences[:2]) + "."
    else:
        summary = text

    summary = "Summary: " + summary.strip()

    return jsonify({"result": summary})


# 🔹 PDF UPLOAD + SUMMARIZATION
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = file.filename

    text = ""

    if filename.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8")

    else:
        return jsonify({"result": "Unsupported file type!"})

    summary = "Summary: " + text[:200]

    return jsonify({"result": summary})

if __name__ == "__main__":
    app.run(debug=True)