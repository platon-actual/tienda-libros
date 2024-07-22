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
# Se agregan los directorios src y templates

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "secreto"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    cursor.close()
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
    
    cursor.execute("SELECT * FROM editores ORDER BY editor_id ASC")
    listaEditores = cursor.fetchall()
    insertEditores = []
    columnNames2 = [column[0] for column in cursor.description]
    for editor in listaEditores:
        insertEditores.append(dict(zip(columnNames2, editor)))


    cursor.close()
    conn.close()
    return render_template('ediciones.html', ediciones=insertObject, editores=insertEditores)

def archivo_valido(nombre):
    return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ediciones', methods=['POST', 'GET'])
def alta_edicion():
    if request.method == 'POST':
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
            # return render_template('ediciones.html', archivo=nombre_archivo)
        else:
            flash("Extensiones permitidas jpg y png y poco más")
            # return redirect(request.url)

        # guardar datos de la edición en la base
        editor = request.form.get('editores')
        numero_edicion = request.form['numero_edicion']
        fecha_edicion = request.form['fecha_edicion']
        flash(fecha_edicion)
        stock = request.form['stock']
        isbn = request.form['isbn']
        # guardar nombre_archivo en la base # TODO agregar nombre de archivo único
        url_imagen_tapa = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(archivo.filename))
        url_imagen_trasera = ''
        paginas = request.form['paginas']
        tamanio = request.form['tamanio']
        
        
        
        #if 1!=1: # mensaje_usuario and mensaje_texto:
        if editor and  fecha_edicion and stock and isbn and url_imagen_tapa and paginas and tamanio:
            flash("Entrando al insert...")
            conn = db.db_connect()
            cursor = conn.cursor()
            sql = "INSERT INTO ediciones (editor_id, numero_edicion, fecha_edicion, stock, isbn, url_imagen_tapa, url_imagen_trasera, paginas, tamanio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (editor, numero_edicion, fecha_edicion, stock, isbn, url_imagen_tapa, url_imagen_trasera, paginas, tamanio)

            cursor.execute(sql, data)
            conn.commit()

            cursor.close()
            conn.close()
            flash("saliendo del insert...")
    
    conn = db.db_connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ediciones ORDER BY edicion_id ASC")
    miResultado = cursor.fetchall()
    # Convertir los datos a diccionario
    insertEdiciones = []
    columnNames = [column[0] for column in cursor.description]
    for registro in miResultado:
        insertEdiciones.append(dict(zip(columnNames, registro)))
    
    cursor.execute("SELECT * FROM editores ORDER BY editor_id ASC")
    listaEditores = cursor.fetchall()
    insertEditores = []
    columnNames2 = [column[0] for column in cursor.description]
    for editor in listaEditores:
        insertEditores.append(dict(zip(columnNames2, editor)))


    cursor.close()
    conn.close()
    # return render_template ('ediciones.html', methods=['GET'])
    # return redirect(request.url) # esto tira error... no entiendo bien porque
    return render_template('ediciones.html', ediciones=insertEdiciones, editores=insertEditores)


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
