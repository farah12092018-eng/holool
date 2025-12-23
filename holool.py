from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

HTML = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>Holool AI</title>
<style>
body {
    font-family: Arial;
    background: #0f172a;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.box {
    width: 400px;
}
textarea {
    width: 100%;
    height: 100px;
    margin-bottom: 10px;
}
button {
    width: 100%;
    padding: 10px;
    background: #22c55e;
    border: none;
    cursor: pointer;
}
pre {
    white-space: pre-wrap;
    margin-top: 10px;
}
</style>
</head>
<body>
<div class="box">
<h2>Holool AI</h2>
<textarea id="q" placeholder="اكتب سؤالك هنا"></textarea>
<button onclick="send()">إرسال</button>
<pre id="a"></pre>
</div>

<script>
function send() {
    const q = document.getElementById("q");
    const a = document.getElementById("a");
    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: q.value})
    })
    .then(r => r.json())
    .then(d => {
        a.textContent = d.answer;
        q.value = "";
    });
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "اكتب سؤال أولاً"})

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=question
    )

    answer = response.output_text
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run()
