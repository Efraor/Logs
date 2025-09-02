# Funciones de base de datos para logging

import sqlite3
import os
from datetime import datetime, timezone

DB_FILE = '../db/logs.db'

def init_db():
    """Inicializa la base de datos con la tabla de logs, incluyendo 'received_at'"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            received_at TEXT NOT NULL,
            service TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos y tabla 'logs' creada correctamente")


def insert_log(timestamp, service, severity, message):
    """Inserta un nuevo log en la base de datos"""
    # Auto-inicializar DB si no existe
    if not os.path.exists(DB_FILE):
        print(f"Base de datos no existe. Creando {DB_FILE}...")
        init_db()
        print("✓ Base de datos creada")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    received_at = datetime.now(timezone.utc).isoformat()

    
    try:
        cursor.execute('''
    INSERT INTO logs (timestamp, received_at, service, severity, message)
    VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, received_at, service, severity, message))
        
        conn.commit()
        print(f"✓ Log guardado: {service} - {severity} - {message[:50]}...")
    except Exception as e:
        print(f"✗ Error guardando log: {e}")
        raise
    finally:
        conn.close()

def geat_all_logs():
    """Obtiene todos los logs"""
    if not os.path.exists(DB_FILE):
        return []
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT timestamp, service, severity, message FROM logs ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    
    conn.close()
    
    # Convertir a lista de diccionarios
    logs = []
    for row in rows:
        logs.append({
            'timestamp': row[0],
            'service': row[1],
            'severity': row[2],
            'message': row[3]
        })
    
    return logs

def get_logs_filtered(service=None, severity=None, 
                    timestamp_start=None, timestamp_end=None, 
                    received_at_start=None, received_at_end=None):
    if not os.path.exists(DB_FILE):
        return []
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    query = 'SELECT timestamp, received_at, service, severity, message FROM logs WHERE 1=1'
    params = []

    if service:
        query += ' AND service = ?'
        params.append(service)
    if severity:
        query += ' AND severity = ?'
        params.append(severity)
    if timestamp_start:
        query += ' AND timestamp >= ?'
        params.append(timestamp_start)
    if timestamp_end:
        query += ' AND timestamp <= ?'
        params.append(timestamp_end)
    if received_at_start:
        query += ' AND received_at >= ?'
        params.append(received_at_start)
    if received_at_end:
        query += ' AND received_at <= ?'
        params.append(received_at_end)

    query += ' ORDER BY timestamp DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for row in rows:
        logs.append({
            'timestamp': row[0],
            'received_at': row[1],
            'service': row[2],
            'severity': row[3],
            'message': row[4]
        })
    
    return logs


init_db()
print("Todo correcto")
