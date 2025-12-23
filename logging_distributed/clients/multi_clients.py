# Script para enviar logs simultáneamente desde varios clientes

import requests, random, threading
from datetime import datetime

SERVER = "http://127.0.0.1:5000"
API_TOKEN = "MiTokenSecreto123"

services = ["Auth","payments","orders"]

severities = ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"]

num_logs = 100 # Cantidad de logs por servicio

def iso_now():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def send_logs(service, num_logs):
    for i in range(1, num_logs + 1):
        payload = {
            "timestamp": iso_now(),
            "service": service,
            "severity": random.choice(severities),
            "message": f"log #{i} desde {service} - prueba {random.randint(100,1000)}"
        }
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Token {API_TOKEN}"
        }
        try:
            r = requests.post(f"{SERVER}/logs", json=payload, headers=header, timeout=5)
            print(f"[{service}] {i}/{num_logs} -> {r.status_code} - {r.json()}")
        except requests.exceptions.RequestException as e:
            print(f"[{service}] {i}/{num_logs} - Error: {e}")

if __name__ == "__main__":
    threads = []
    for service in services:
        t = threading.Thread(target= send_logs, args=(service, num_logs))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    
    print("Todos los servicios terminaron de enviar logs.")

