from flask import Flask, flash, render_template, request, redirect, url_for
# Importamos Flask para comenzar el proyecto. Para instalar flask en la terminal escribir pip install flask
from werkzeug.utils import secure_filename
import urllib.request
import os
# Importamos os para acceder a los directorios

import database as db
# Importamos la conexión a base de datos con alias db

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

template_dir = os.path.join(template_dir, "src", "templates")
# Le agregamos los directorios src y templates

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "secreto"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# vamos a generar nuestra primer ruta para poder ejecutar
# Ruta de la app
#@app.route('/') es un decorador. El decorador vincula una función específica del sitio web
# la función home() será la encargada de que se ejecute la página principal

# Importante a la primer línea de código (from flask import Flask) agregar render_template

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

@app.route('/editores', methods=['GET'])
def editores():
    conn = db.db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM editores ORDER BY editor_id ASC")
    miResultado = cursor.fetchall()
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for registro in miResultado:
        insertObject.append(dict(zip(columnNames, registro)))
    cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
    conn.close()
    return render_template('editores.html', editores=insertObject)

@app.route('/ediciones', methods=['GET'])
def ediciones():
    conn = db.db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ediciones ORDER BY edicion_id ASC")
    miResultado = cursor.fetchall()
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for registro in miResultado:
        insertObject.append(dict(zip(columnNames, registro)))
    cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
    conn.close()
    return render_template('ediciones.html', ediciones=insertObject)

def archivo_valido(nombre):
    return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ediciones', methods=['POST'])
def alta_edicion():

    if 'portada' not in request.files:
        flash('no hay archivo de imágen')
        return redirect(request.url)
    archivo = request.files['portada']
    flash(archivo)
    if archivo.filename == '':
        flash('No se seleccionó imágen.')
        return redirect(request.url)
    
    if archivo and archivo_valido(archivo.filename):
        nombre_archivo = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], nombre_archivo))
        flash("Portada subida exitosamente!")
        return render_template('ediciones.html', archivo=nombre_archivo)
    else:
        flash("Extensiones permitidas jpg y png y poco más")
        return redirect(request.url)

    conn = db.db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ediciones ORDER BY edicion_id ASC")
    miResultado = cursor.fetchall()
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for registro in miResultado:
        insertObject.append(dict(zip(columnNames, registro)))
    cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
    conn.close()
    return render_template('ediciones.html', ediciones=insertObject)


@app.route('/foro', methods=['POST'])
def nuevo_mensaje_foro():
    mensaje_usuario = request.form['nombre']
    mensaje_texto = request.form['mensaje']
    
    if mensaje_usuario and mensaje_texto:
        conn = db.db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO mensajes (autor, mensaje) VALUES (%s, %s)"
        data = (mensaje_usuario, mensaje_texto)

        # hay que ejecutar la consulta y luego hacer el commit
        cursor.execute(sql, data)
        conn.commit()
        cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
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
    cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
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

        # hay que ejecutar la consulta y luego hacer el commit
        cursor.execute(sql, data)
        conn.commit()
        cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
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
        cursor.close() # Es una buena práctica cerrar los cursores luego de usarlos
        conn.close()
    return redirect (url_for('usuarios'))


# Ejecución directa del archivo, en el puerto 4000 (http://localhost:4000)
if __name__ == '__main__':
    app.run(debug=True, port=4000)
