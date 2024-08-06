# Copyright Ramiro Iván Ríos 2024
from __main__ import app
import os, uuid
import database as db
from flask import request, render_template, flash, redirect
from werkzeug.utils import secure_filename

#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

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
        
        # le doy un nombre único al archivo de imágen con uuid.uuid4().hex()
        nombre_archivo, extension_archivo = os.path.splitext(archivo.filename)
        nombre_final_archivo = uuid.uuid4().hex + extension_archivo
        flash(extension_archivo)
        flash(nombre_final_archivo)
        if archivo.filename == '':
            flash('No se seleccionó imágen.')
            return redirect(request.url)
        
        if archivo and archivo_valido(archivo.filename):
            

            archivo.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], nombre_final_archivo))
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
        url_imagen_tapa = os.path.join(app.config['UPLOAD_FOLDER'], nombre_final_archivo)
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
