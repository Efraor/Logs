# Funciones de autenticación y validación de tokens

from flask import request, jsonify

API_TOKEN = "MiTokenSecreto123"

def validate_token():
    token = request.headers.get("Authorization", "")
    
    # Verificar que el token tenga el formato correcto "Token XXXXX"
    if not token.startswith("Token "):
        return jsonify({"error": "Quien sos, bro?"}), 401
    
    # Extraer el token removiendo el prefijo "Token "
    actual_token = token[6:]  # Remover "Token " (6 caracteres)
    
    if actual_token != API_TOKEN:
        return jsonify({"error": "Quien sos, bro?"}), 401
    
    return None