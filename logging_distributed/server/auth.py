# Funciones de autenticación y validación de tokens

from flask import request, jsonify

API_TOKEN = "MiTokenSecreto123"

def validate_token():
    token = request.headers.get("Authorization", "")
    if not token or token.replace("Token", "") != API_TOKEN:
        return jsonify({"error": "Quien sos, bro?"}), 401
    return None