from flask import Flask, jsonify, request, redirect
import stripe
import random
import string

app = Flask(__name__)

# ====== Stripe ======
stripe.api_key = "sk_test_XXXXXXXXXXXXXXXXXXXX"  # مفتاح Stripe السري

PRICE_ID = "price_XXXXXXXXXXXXXXXX"  # سعر الاشتراك 5$ شهري

# ====== أكواد ======
FOUNDER_CODE = "FOUNDER-9999"  # كودك أنت (مجاني)
active_codes = set()

def generate_code():
    return "SUB-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ====== الصفحة الرئيسية ======
@app.route("/")
def home():
    return """
    <h2>Holool AI</h2>
    <p>اشتراك شهري: 5$</p>
    <button onclick="pay()">اشترك الآن</button>

    <script>
    function pay(){
      fetch('/create-checkout')
      .then(r=>r.json())
      .then(d=>window.location=d.url)
    }
    </script>
    """

# ====== إنشاء الدفع ======
@app.route("/create-checkout")
def checkout():
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": PRICE_ID, "quantity": 1}],
        success_url="https://YOUR-SITE.onrender.com/success",
        cancel_url="https://YOUR-SITE.onrender.com"
    )
    return jsonify(url=session.url)

# ====== بعد الدفع ======
@app.route("/success")
def success():
    code = generate_code()
    active_codes.add(code)
    return f"""
    <h3>✅ تم الاشتراك</h3>
    <p>كودك:</p>
    <h2>{code}</h2>
    """

# ====== التحقق من الكود ======
@app.route("/check", methods=["POST"])
def check():
    code = request.json.get("code")

    if code == FOUNDER_CODE:
        return jsonify(ok=True, role="founder")

    if code in active_codes:
        return jsonify(ok=True, role="user")

    return jsonify(ok=False)

if __name__ == "__main__":
    app.run()
