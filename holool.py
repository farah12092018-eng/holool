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
body { font-family: Arial; background:#f5f5f5; padding:40px; }
input, button { padding:10px; width:100%; margin-top:10px; }
#answer { margin-top:20px; background:white; padding:15px; }
</style>
</head>
<body>
<h2>اسألني</h2>
<input id="q" placeholder="اكتب سؤالك هنا">
<button onclick="ask()">اسأل</button>
<div id="answer"></div>

<script>
async function ask(){
  const q = document.getElementById("q").value;
  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: q})
  });
  const data = await res.json();
  document.getElementById("answer").innerText = data.answer;
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

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=question
    )

    answer = response.output_text
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
