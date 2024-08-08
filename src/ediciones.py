# Copyright Ramiro Iván Ríos 2024
from __main__ import app
import os, uuid
import database as db
from flask import request, render_template, flash, redirect
from werkzeug.utils import secure_filename

#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

@app.route('/alta_libros', methods=['GET'])
def alta_libros():
    conn = db.db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM editores ORDER BY editor_id ASC")
    listaEditores = cursor.fetchall()
    insertEditores = []
    columnNames2 = [column[0] for column in cursor.description]
    for editor in listaEditores:
        insertEditores.append(dict(zip(columnNames2, editor)))


    cursor.close()
    conn.close()
    return render_template('altas/libros.html', editores=insertEditores)

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
    
    cursor.close()
    conn.close()
    return render_template('ediciones.html', ediciones=insertObject)

def archivo_valido(nombre):
    return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ediciones', methods=['POST', 'GET'])
def alta_edicion():
    if request.method == 'POST':
        if 'portada' not in request.files:
            flash('no hay archivo de imágen')
            return redirect(request.url)
        tapa = request.files['portada']
        tapa_trasera = request.files['contratapa']
        
        # le doy un nombre único al archivo de imágen con uuid.uuid4().hex()
        nombre_tapa, extension_tapa = os.path.splitext(tapa.filename)
        nombre_tapa_t, extension_tapa_t = os.path.splitext(tapa_trasera.filename)

        nombre_final_tapa = uuid.uuid4().hex + extension_tapa
        nombre_final_tapa_t = uuid.uuid4().hex + extension_tapa_t

        if tapa.filename == '' and tapa_trasera.filename == '':
            flash('No se seleccionó imágen.')
            return redirect(request.url)
        
        if tapa and archivo_valido(tapa.filename):
            # guardo en el sistema local las imágenes con un nombre uuid4 y la extensión original
            tapa.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], nombre_final_tapa))
            if tapa_trasera:
                tapa_trasera.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], nombre_final_tapa_t))

        else:
            flash("Extensiones permitidas: .jpeg, .jpg y .png")

        # guardar datos del libro en variables
        autor = request.form['autor']
        titulo = request.form['titulo']

        # guardar datos de la edición en variables
        editor = request.form.get('editores')
        numero_edicion = request.form['numero_edicion']
        nombre_edicion = request.form['nombre_edicion']
        fecha_edicion = request.form['fecha_edicion']
        flash(fecha_edicion)
        stock = request.form['stock']
        isbn = request.form['isbn']
        # guardar url de archivos de imágenes en las variables
        url_imagen_tapa = os.path.join(app.config['UPLOAD_FOLDER'], nombre_final_tapa)
        url_imagen_tapa_t = os.path.join(app.config['UPLOAD_FOLDER'], nombre_final_tapa_t)
        paginas = request.form['paginas']
        tamanio = request.form['tamanio']
        
        # guardar en SQL el libro y la edición
        if editor and  fecha_edicion and stock and isbn and url_imagen_tapa and paginas and tamanio:
            
            conn = db.db_connect()
            cursor = conn.cursor()

            sql = "INSERT INTO ediciones (editor_id, numero_edicion, nombre_edicion, fecha_edicion, stock, isbn, url_imagen_tapa, url_imagen_trasera, paginas, tamanio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (editor, numero_edicion, nombre_edicion, fecha_edicion, stock, isbn, url_imagen_tapa, url_imagen_tapa_t, paginas, tamanio)
            cursor.execute(sql, data)
            conn.commit()

            sql = "INSERT INTO libros (autor, titulo, fecha_publicacion, edicion_id) VALUES (%s, %s, %s, %s)"
            data = (autor, titulo, '', cursor.lastrowid)
            cursor.execute(sql, data)
            conn.commit()

            cursor.close()
            conn.close()
            
    
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
