from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import sqlite3
from datetime import datetime
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔑 حط مفتاح OpenAI هون
client = OpenAI(api_key="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")

# 🎁 عدد الأسئلة المجانية
FREE_LIMIT = 10

# 💰 كود اشتراك (1 دينار – استخدام مرة وحدة)
PREMIUM_CODE = "mosa1212322012013"


def init_db():
    conn = sqlite3.connect("chats.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            questions INTEGER DEFAULT 0,
            premium INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT,
            reply TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        return redirect(f"/chat?name={name}")
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html", name=request.args.get("name"))


@app.route("/ask", methods=["POST"])
def ask():
    global PREMIUM_CODE

    data = request.get_json()
    msg = data.get("message")
    name = data.get("name", "مستخدم")

    conn = sqlite3.connect("chats.db")
    c = conn.cursor()

    c.execute("SELECT questions, premium FROM users WHERE name=?", (name,))
    row = c.fetchone()

    if row is None:
        c.execute(
            "INSERT INTO users (name, questions, premium) VALUES (?, 0, 0)",
            (name,)
        )
        questions = 0
        premium = 0
    else:
        questions = row[0]
        premium = row[1]

    # ⭐ تفعيل Premium بالكود
    if msg == PREMIUM_CODE:
        c.execute(
            "UPDATE users SET premium = 1 WHERE name=?",
            (name,)
        )

        PREMIUM_CODE = "USED"  # تعطيل الكود بعد الاستخدام

        conn.commit()
        conn.close()
        return jsonify({
            "reply": "🎉 تم تفعيل الاشتراك Premium!\nصار عندك استخدام غير محدود ♾️"
        })

    # 🚫 الحد المجاني
    if premium == 0 and questions >= FREE_LIMIT:
        conn.close()
        return jsonify({
            "reply": "🚫 خلصت 10 أسئلة مجانية.\nالاشتراك = 1 دينار 💰"
        })

    # 🤖 الذكاء الاصطناعي
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
أنت مساعد عربي ذكي يساعد الناس على حل مشاكلهم
بأسلوب إنساني وتعاطفي.

المشكلة:
{msg}
"""
    )

    reply = response.output_text

    if premium == 0:
        c.execute(
            "UPDATE users SET questions = questions + 1 WHERE name=?",
            (name,)
        )

    c.execute(
        "INSERT INTO chats (name, message, reply, created_at) VALUES (?, ?, ?, ?)",
        (name, msg, reply, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
