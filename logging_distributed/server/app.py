# Servidor Flask principal

from flask import Flask, request, jsonify
from db import insert_log, geat_all_logs, get_logs_filtered
from datetime import datetime, timezone
from auth import validate_token

def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def add_log():
    try:
        print(f"Recibida petición POST a /logs")
        
        auth_error = validate_token()
        if auth_error:
            return auth_error
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        service = data.get("service")
        severity = data.get("severity")
        message = data.get("message")
        timestamp = data.get("timestamp")  # <-- obtener timestamp del cliente
        
        if not all([service, severity, message]):
            return jsonify({"error":"Missing fields"}), 400
        
        # Si el cliente no envía timestamp, lo generamos
        if not timestamp:
            from datetime import datetime, timezone
            timestamp = datetime.now(timezone.utc).isoformat()
        
        insert_log(timestamp, service, severity, message)
        
        return jsonify({"message":"Log saved"}), 201
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/logs", methods=["GET"])
def list_logs():
    try:
        auth_error = validate_token()
        if auth_error:
            return auth_error

        # Filtros opcionales
        service = request.args.get("service")
        severity = request.args.get("severity")
        timestamp_start = request.args.get("timestamp_start")
        timestamp_end = request.args.get("timestamp_end")
        received_at_start = request.args.get("received_at_start")
        received_at_end = request.args.get("received_at_end")

        logs = get_logs_filtered(
            service=service,
            severity=severity,
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end,
            received_at_start=received_at_start,
            received_at_end=received_at_end
        )

        return jsonify({
            "count": len(logs),
            "logs": logs
        })
    
    except Exception as e:
        print(f"Error en list_logs: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/", methods=["GET"])
def ok():
    return jsonify({"status": "ok", "time": iso_now()})

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)