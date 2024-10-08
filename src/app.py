# Copyright Ramiro Iván Ríos 2024

from flask import Flask, flash, render_template, request, redirect, url_for
# Importamos Flask para comenzar el proyecto. Para instalar flask en la terminal escribir pip install flask
import urllib.request
import os
# Importamos os para acceder a los directorios

import database as db
# Importamos la conexión a base de datos con alias db

UPLOAD_FOLDER = 'static/uploads'

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

template_dir = os.path.join(template_dir, "src", "templates")
# Se agregan los directorios src y templates

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "secreto"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Agrego e importo las rutas, divididas en archivos .py
import editores, ediciones

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/foro', methods=['POST'])
def nuevo_mensaje_foro():
    mensaje_usuario = request.form['nombre']
    mensaje_texto = request.form['mensaje']
    
    if mensaje_usuario and mensaje_texto:
        conn = db.db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO mensajes (autor, mensaje) VALUES (%s, %s)"
        data = (mensaje_usuario, mensaje_texto)

        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()
    return redirect (url_for('foro'))

@app.route('/usuarios', methods=['GET'])
def usuarios():
    conn = db.db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    miResultado = cursor.fetchall()
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for registro in miResultado:
        insertObject.append(dict(zip(columnNames, registro)))
    cursor.close()
    conn.close() 
    return render_template('usuarios.html', data=insertObject)

# Ruta para guardar usuarios en la base de datos.
@app.route('/alta_usuario', methods=['POST'])
def addUser():
    user_mail = request.form['mail']
    user_name = request.form['nombre']
    user_pass = request.form['clave']

    if user_mail and user_name and user_pass:
        conn = db.db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (mail, nombre, clave) VALUES (%s, %s, %s)"
        data = (user_mail, user_name, user_pass)

        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()
    return redirect (url_for('usuarios'))

# Ruta para borrar usuarios
@app.route('/borrarusuario/<string:id>')
def borrar_usuario(id):
    conn = db.db_connect()
    cursor = conn.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    conn.commit()

    cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
    conn.close() # Es una práctica básica cerrar la conexión
    return redirect (url_for('usuarios'))

# Ruta para modificar datos
@app.route('/editar_usuario/<string:id>', methods=['POST'])
def editar(id):
    user_mail = request.form['mail']
    user_name = request.form['nombre']
    user_pass = request.form['clave']

    if user_mail and user_name and user_pass:
        conn = db.db_connect()
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET mail = %s, nombre = %s, clave = %s WHERE id=%s"
        data = (user_mail, user_name, user_pass, id)

        # hay que ejecutar la consulta y luego hacer el commit
        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()
    return redirect (url_for('usuarios'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
