# Funciones de conexión y operaciones en la base de datos

import sqlite3 as sql

DB_File = '../db/logs.db'

def connection():
    conn = sql.connect(DB_File)
    conn.row_factory = sql.Row
    return conn

def insert_log (service, severity, message):
    # Inserta un log en la DB
    coon = connection()
    c = coon.cursor()
    query = 'INSERT INTO logs(service, severity, message) VALUES (?, ?, ?)'
    c.execute(query,
            (service, severity, message))
    coon.commit()
    coon.close()

def geat_all_logs():
    # Devuelve todos los logs
    coon = connection()
    c = coon.cursor()
    query = 'SELECT * FROM logs ORDER BY id'
    c.execute(query)
    rows = c.fetchall()
    coon.close()
    return [dict(row) for row in rows]

def get_logs_filtered(service = None, severity= None):
    # Devuelve logs filtrados por service y/o severity
    conn = connection()
    c = conn.cursor()

    query = "SELECT * FROM logs WHERE 1=1"
    params= []

    if service:
        query += " AND service = ?"
        params.append(service)
    if severity:
        query += " AND severity = ?"
        params.append(severity)

    query += " ORDER BY id DESC"
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]




