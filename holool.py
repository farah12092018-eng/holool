from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "login": ["google"]})


@app.route("/login/google", methods=["POST"])
def login_google():
    data = request.json
    token = data.get("id_token")

    if not token:
        return jsonify({"error": "no token"}), 400

    try:
        info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        user = {
            "id": info["sub"],
            "email": info["email"],
            "name": info.get("name", "")
        }

        jwt_token = jwt.encode(
            user,
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        return jsonify({"token": jwt_token, "user": user})

    except Exception as e:
        return jsonify({"error": "invalid google token"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
