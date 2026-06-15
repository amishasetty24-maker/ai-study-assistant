from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from google import genai
import os
import time

app = Flask(__name__)
CORS(app)

# Gemini API Key from Render Environment Variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


# ROOT ROUTE
@app.route("/")
def home():
    return "Backend is running!"


def generate_summary(prompt):
    """
    Retry Gemini request up to 3 times.
    Helps with temporary 503 overload errors.
    """
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < 2:
                time.sleep(3)
            else:
                raise


# TEXT SUMMARIZATION
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "result": "Please enter some text."
            })

        if not client:
            return jsonify({
                "result": "Gemini API key not configured."
            }), 500

        prompt = f"""
You are an AI Study Assistant.

Analyze the study notes below and provide:

1. Summary
2. 3-5 Key Points
3. Important Keywords

Study Notes:
{text[:10000]}
"""

        result = generate_summary(prompt)

        return jsonify({
            "result": result
        })

    except Exception as e:
        print("Summarize Error:", e)

        return jsonify({
            "result": "AI service is temporarily busy. Please try again in a minute."
        }), 500

@app.route("/flashcards", methods=["POST"])
def flashcards():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "result": "Please enter some text."
            })

        if not client:
            return jsonify({
                "result": "Gemini API key not configured."
            }), 500

        prompt = f"""
You are a study assistant.

Generate 5 study flashcards.

Format:

Q: Question
A: Answer

Study Notes:
{text[:10000]}
"""

        result = generate_summary(prompt)

        return jsonify({
            "result": result
        })

    except Exception:
        return jsonify({
            "result": "AI service is temporarily busy. Please try again."
        }), 500

@app.route("/quiz", methods=["POST"])
def quiz():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "result": "Please enter some text."
            })

        if not client:
            return jsonify({
                "result": "Gemini API key not configured."
            }), 500

        prompt = f"""
You are a study assistant.

Create 5 multiple-choice questions (MCQs) from the study notes.

Rules:
- Each question should have 4 options (A, B, C, D).
- Show the correct answer after each question.
- Make questions useful for exam preparation.

Study Notes:
{text[:10000]}
"""

        result = generate_summary(prompt)

        return jsonify({
            "result": result
        })

    except Exception:
        return jsonify({
            "result": "AI service is temporarily busy. Please try again."
        }), 500
# PDF UPLOAD + SUMMARIZATION
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({
                "result": "No file uploaded."
            }), 400

        file = request.files["file"]

        text = ""

        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(file)

            for page in reader.pages:
                content = page.extract_text()

                if content:
                    text += content

        else:
            text = file.read().decode("utf-8")

        if not text.strip():
            return jsonify({
                "result": "No text found in file."
            })

        if not client:
            return jsonify({
                "result": "Gemini API key not configured."
            }), 500

        prompt = f"""
You are an AI Study Assistant.

Analyze the study notes below and provide:

1. Summary
2. 3-5 Key Points
3. Important Keywords

Study Notes:
{text[:10000]}
"""

        result = generate_summary(prompt)

        return jsonify({
            "result": result
        })

    except Exception as e:
        print("Upload Error:", e)

        return jsonify({
            "result": "AI service is temporarily busy. Please try again in a minute."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)