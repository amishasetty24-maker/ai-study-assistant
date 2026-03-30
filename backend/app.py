from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader

app = Flask(__name__)

# ✅ Enable CORS properly
CORS(app)

# ✅ Handle preflight (OPTIONS) requests
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

# 🔹 TEXT SUMMARIZATION
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")

    print("Received:", text)

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


# ✅ Force CORS headers in every response
@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


# ✅ Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)