# Script para crear la base de datos y tablas

import sqlite3

DB_FILE = '../db/logs.db'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    service TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ Tabla 'logs' creada correctamente")