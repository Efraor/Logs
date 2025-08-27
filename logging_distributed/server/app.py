# Servidor Flask principal

from flask import Flask, request, jsonify
from db import insert_log, geat_all_logs, get_logs_filtered
from datetime import datetime
from auth import validate_token

def iso_now():
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'z'

app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def add_log():
    auth_error = validate_token()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    service = data.get("service")
    severity = data.get("severity")
    message = data.get("message")

    if not all([service, severity, message]):
        return jsonify({"error":"Missing fields"}), 400
    
    insert_log(service, severity, message)
    
    return jsonify({"message":"Log saved"}), 201

@app.route("/logs", methods=["GET"])
def list_logs():
    # Validación del token online
    auth_error = validate_token()
    if auth_error:
        return auth_error
    
    # Si se pasasn filtros devuelve logs filtrados, sino todos
    service = request.args.get("service")
    severity = request.args.get("severity")

    if service or severity:
        logs = get_logs_filtered(service, severity)
    else:
        logs = geat_all_logs()
    return jsonify({
        "count": len(logs),
        "logs": logs
    })

@app.route("/", methods=["GET"])
def ok():
    return jsonify({"status": "ok", "time": iso_now()})

if __name__ == "__main__":
    app.run(debug=True)





