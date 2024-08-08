# Copyright Ramiro Iván Ríos 2024
from __main__ import app
import database as db
from flask import request, render_template

@app.route('/editores', methods=['GET', 'POST'])
def editores():
    conn = db.db_connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        domicilio = request.form['domicilio']
        telefono = request.form['telefono']
        notas = request.form['notas']
        sql = "INSERT INTO editores (nombre, correo, domicilio, telefono, notas) VALUES (%s, %s, %s, %s, %s)"
        data = (nombre, correo, domicilio, telefono, notas)

        cursor.execute(sql, data)
        conn.commit()
    
    cursor.execute("SELECT * FROM editores ORDER BY editor_id ASC")
    miResultado = cursor.fetchall()
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for registro in miResultado:
        insertObject.append(dict(zip(columnNames, registro)))

    cursor.close()
    conn.close()
    return render_template('editores.html', editores=insertObject)