from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from google import genai
import os

app = Flask(__name__)
CORS(app)

# Gemini API Key from Render environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


# ROOT ROUTE
@app.route("/")
def home():
    return "Backend is running!"


# TEXT SUMMARIZATION
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"result": "Please enter some text."})

        if not client:
            return jsonify({"result": "Gemini API key not configured."}), 500

        prompt = f"""
        Summarize the following study notes in a concise and student-friendly way:

        {text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "result": response.text
        })

    except Exception as e:
        return jsonify({
            "result": f"Error: {str(e)}"
        }), 500


# PDF UPLOAD + SUMMARIZATION
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"result": "No file uploaded."}), 400

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

        if not text.strip():
            return jsonify({"result": "No text found in file."})

        if not client:
            return jsonify({"result": "Gemini API key not configured."}), 500

        prompt = f"""
        You are a study assistant.

       Create:
       1. A concise summary.
       2. 3-5 key points.
       3. Important keywords.

       Study Notes:
       {text}
       """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return jsonify({
            "result": response.text
        })

    except Exception:
    return jsonify({
        "result": "AI service is temporarily busy. Please try again in a few minutes."
    }), 500


if __name__ == "__main__":
    app.run(debug=True)