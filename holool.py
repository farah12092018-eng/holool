from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    q = data.get("question", "")

    r = client.responses.create(
        model="gpt-4.1-mini",
        input=q
    )

    return jsonify({"answer": r.output_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
