from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

HTML = """
<!doctype html>
<html lang="ar">
<head>
<meta charset="utf-8">
<title>Holool</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
}
.container {
    background: white;
    width: 100%;
    max-width: 420px;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}
h2 {
    text-align: center;
    margin-bottom: 20px;
}
input {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 16px;
}
button {
    margin-top: 12px;
    width: 100%;
    padding: 12px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}
button:hover {
    background: #5563d6;
}
#answer {
    margin-top: 20px;
    background: #f4f4f4;
    padding: 15px;
    border-radius: 8px;
    min-height: 40px;
    white-space: pre-wrap;
}
</style>
</head>
<body>

<div class="container">
    <h2>🤖 Holool</h2>
    <input id="q" placeholder="اكتب سؤالك هنا..." />
    <button onclick="ask()">اسأل</button>
    <div id="answer"></div>
</div>

<script>
async function ask(){
    const input = document.getElementById("q");
    const answerDiv = document.getElementById("answer");
    const question = input.value.trim();

    if(!question) return;

    input.value = "";
    answerDiv.innerText = "⏳ جاري التفكير...";

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({question})
        });
        const data = await res.json();
        answerDiv.innerText = data.answer;
    } catch {
        answerDiv.innerText = "❌ صار خطأ";
    }
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
    question = request.json.get("question", "")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=question
    )

    return jsonify({"answer": response.output_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
