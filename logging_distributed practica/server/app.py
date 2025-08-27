# Servidor Flask principal

# Ejercicio 1 – Crear el servidor básico

# Crea un servidor en Flask con un solo endpoint /ping que responda "pong".
# 👉 Objetivo: Confirmar que tu servidor está funcionando.

"""
from flask import Flask

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "Pong"

if __name__ == "__main__":
    app.run(debug=True)

"""


# Ejercicio 2 – Endpoint para logs (sin base de datos todavía)
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/logs", methods = ['POST'])
def receive_logs():
    data = request.get_json() # recibe el JSON del cliente
    print(f"Nuevo log recibido")
    print(f'service: {data.get('service')}')
    print(f'severity: {data.get('severity')}')
    print(f'message: {data.get('message')}')
    print("-"*20)

    return jsonify({"status": "ok", "message":"Log recibido"}), 200

if __name__ == '__main__':
    app.run(debug=True)

"""

# Ejercicio 3 – Guardar logs en memoria
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


memory = []

@app.route("/logs", methods = ['POST'])
def receive_logs():
    data = request.get_json() # recibe el JSON del cliente
    if not data:
        return jsonify({"status": "error", "message": "No se recibió JSON"}),400
    
    print(f"Nuevo log recibido")
    print(f'service: {data.get('service')}')
    print(f'severity: {data.get('severity')}')
    print(f'message: {data.get('message')}')
    print("-"*20)

    memory.append({"Service":data.get('service'),  "severity": data.get('severity'), "message":data.get('message')})
    print(memory)
    return jsonify({"status": "ok", "message":"Log recibido"}), 200

@app.route("/logs", methods = ['GET'])
def get_logs():
    return jsonify(memory), 200

if __name__ == '__main__':
    app.run(debug=True)
"""


# Ejercicio 4 – Guardar logs en una base de datos
"""

from flask import Flask, request, jsonify
from db import insert_log, geat_all_logs

app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def add_log():
    data = request.get_json()
    service = data.get("service")
    severity = data.get("severity")
    message = data.get("message")

    if not all([service, severity, message]):
        return jsonify({"error":"Missing fields"}), 400
    
    insert_log(service, severity, message)
    return jsonify({"message":"Log saved"}), 201

@app.route("/logs", methods=["GET"])
def list_logs():
    logs = geat_all_logs()
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)

    
"""

# Ejercicio 5 – Filtros en la consulta

"""
from flask import Flask, request, jsonify
from db import insert_log, geat_all_logs, get_logs_filtered

app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def add_log():
    data = request.get_json()
    service = data.get("service")
    severity = data.get("severity")
    message = data.get("message")

    if not all([service, severity, message]):
        return jsonify({"error":"Missing fields"}), 400
    
    insert_log(service, severity, message)
    
    return jsonify({"message":"Log saved"}), 201

@app.route("/logs", methods=["GET"])
def list_logs():
    # Si se pasasn filtros devuelve logs filtrados, sino todos
    service = request.args.get("service")
    severity = request.args.get("severity")

    if service or severity:
        logs = get_logs_filtered(service, severity)
    else:
        logs = geat_all_logs()
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
"""


#Ejercicio 6 – Cliente simulador de servicios
#Crea un script en Python que simule servicios enviando logs al servidor:
"Como es un cliente utilizamos el mismo servidor del 5 ejercicio"
"""

from flask import Flask, request, jsonify
from db import insert_log, geat_all_logs, get_logs_filtered

app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def add_log():
    data = request.get_json()
    service = data.get("service")
    severity = data.get("severity")
    message = data.get("message")

    if not all([service, severity, message]):
        return jsonify({"error":"Missing fields"}), 400
    
    insert_log(service, severity, message)
    
    return jsonify({"message":"Log saved"}), 201

@app.route("/logs", methods=["GET"])
def list_logs():
    # Si se pasasn filtros devuelve logs filtrados, sino todos
    service = request.args.get("service")
    severity = request.args.get("severity")

    if service or severity:
        logs = get_logs_filtered(service, severity)
    else:
        logs = geat_all_logs()
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)


"""

# Ejerciocio 8 todo full

from flask import Flask, request, jsonify
from db import insert_log, geat_all_logs, get_logs_filtered
from datetime import datetime

def iso_now():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


API_TOKEN = "MiTokenSecreto123"

app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def add_log():
    token = request.headers.get("Authorization", "")
    if not token or token.replace("Bearer ", "") != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    
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
    # Validación del token inline
    token = request.headers.get("Authorization", "")
    if not token or token.replace("Bearer ", "") != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    
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

