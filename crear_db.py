import sqlite3
from datetime import datetime

def crear_base_de_datos():
    conn = sqlite3.connect('alumnos.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            aprobado BOOLEAN NOT NULL,
            nota REAL NOT NULL,
            fecha TIMESTAMP NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_base_de_datos()
