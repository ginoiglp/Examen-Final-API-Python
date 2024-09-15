import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Ruta GET para obtener la lista de todos los estudiantes
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    with sqlite3.connect('alumnos.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM alumnos")
        alumnos = cur.fetchall()
        resultado = []
        for alumno in alumnos:
            fecha_obj = datetime.strptime(alumno[5], '%Y-%m-%d %H:%M:%S')  # Convierte a datetime
            resultado.append({
                'id': alumno[0],
                'nombre': alumno[1],
                'apellido': alumno[2],
                'aprobado': alumno[3],
                'nota': alumno[4],
                'fecha': fecha_obj.strftime('%Y-%m-%d %H:%M:%S') # Formatea el datetime
            })
        return jsonify(resultado)

# Ruta GET para obtener un estudiante por su ID
@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    with sqlite3.connect('alumnos.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM alumnos WHERE id=?", (id,))
        alumno = cur.fetchone()
        if alumno:
            return jsonify({
                'id': alumno[0],
                'nombre': alumno[1],
                'apellido': alumno[2],
                'aprobado': alumno[3],
                'nota': alumno[4],
                'fecha': alumno[5].strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({'error': 'Estudiante no encontrado'}), 404

# Ruta POST para crear un nuevo estudiante
@app.route('/alumnos', methods=['POST'])
def create_alumno():
    with sqlite3.connect('alumnos.db') as conn:
        cur = conn.cursor()
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        aprobado = data.get('aprobado')
        nota = data.get('nota')
        fecha = datetime.now()
        if not all([nombre, apellido, aprobado, nota]):
            return jsonify({'error': 'Faltan campos'}), 400
        try:
            cur.execute('''
                INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, apellido, aprobado, nota, fecha))
            conn.commit()
            return jsonify({'mensaje': 'Estudiante creado'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Ruta PUT para actualizar un estudiante
@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    with sqlite3.connect('alumnos.db') as conn:
        cur = conn.cursor()
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        aprobado = data.get('aprobado')
        nota = data.get('nota')
        if not all([nombre, apellido, aprobado, nota]):
            return jsonify({'error': 'Faltan campos'}), 400
        try:
            cur.execute('''
                UPDATE alumnos SET nombre=?, apellido=?, aprobado=?, nota=? WHERE id=?
            ''', (nombre, apellido, aprobado, nota, id))
            conn.commit()
            return jsonify({'mensaje': 'Estudiante actualizado'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Ruta DELETE para eliminar un estudiante
@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    with sqlite3.connect('alumnos.db') as conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM alumnos WHERE id=?", (id,))
            conn.commit()
            return jsonify({'mensaje': 'Estudiante eliminado'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Iniciar la aplicación Flask si se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
