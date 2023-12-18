from flask import render_template
from data_manager import DataManager
# importar dependencias
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash

def conductores_home(data_manager):
    conductores = data_manager.get_conductores()
    return render_template('conductores/index.html', conductores=conductores)

def conductor_form(mongo):
    genero = mongo.db.genero.find()
    trailer = mongo.db.trailer.find()
    return render_template('conductores/agregar.html', trailer=trailer, genero=genero)

def add_conductor(request, data_manager):
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        fecha_nacimiento = request.form.get('nacimiento')
        correo = request.form.get('correo')
        genero_id = int(request.form.get('genero'))
        trailer_id = request.form.get('trailer') 

        # Verificar si la cédula ya existe en la colección de conductores
        if data_manager.conductor_exists(cedula):
            flash('Ya existe un conductor con esa cédula', 'danger')
            return redirect(url_for('formulario_agregar_conductor'))
        else:
            data_manager.add_conductor(nombres, cedula, telefono, fecha_nacimiento, correo, genero_id, trailer_id)
            flash('Conductor agregado correctamente', 'success')
            return redirect(url_for('index_conductores'))
    
    return redirect(url_for('index_conductores'))

def update_conductor(mongo, conductor_id, data_manager):
    conductor = mongo.db.conductores.find_one({'_id': ObjectId(conductor_id)})

    if request.method == 'POST':
        # Obtén los datos actualizados del formulario y actualiza el conductor
        nuevo_nombres = request.form.get('nombres')
        nueva_cedula = request.form.get('cedula')
        nuevo_telefono = request.form.get('telefono')
        nueva_fecha_nacimiento = request.form.get('nacimiento')
        nuevo_correo = request.form.get('correo')
        nuevo_genero_id = int(request.form.get('genero'))
        nuevo_trailer_id = request.form.get('trailer')

        # Verificar si la nueva cédula ya existe en otro conductor
        if nueva_cedula != conductor['cedula'] and data_manager.conductor_exists(nueva_cedula):
            flash('Ya existe un conductor con esa cédula', 'danger')
            return redirect(url_for('editar_conductor', conductor_id=conductor_id))

        data_manager.edit_conductor_by_id(conductor_id, nuevo_nombres, nueva_cedula, nuevo_telefono, nueva_fecha_nacimiento, nuevo_correo, nuevo_genero_id, nuevo_trailer_id)
        flash('Conductor actualizado correctamente', 'success')
        return redirect(url_for('index_conductores'))

    genero = mongo.db.genero.find()
    trailer = mongo.db.trailer.find()

    return render_template('conductores/actualizar.html', conductor=conductor, genero=genero, trailer=trailer)

    
def delete_conductor(conductor_id, mongo, data_manager):
    generos = mongo.db.genero.find()
    trailers = mongo.db.trailer.find()
    conductor = mongo.db.conductores.find_one({'_id': ObjectId(conductor_id)})
    genero_id = conductor.get('genero_id')
    trailer_id = conductor.get('trailer_id')

    genero = mongo.db.genero.find_one({'_id': genero_id})
    trailer = mongo.db.trailer.find_one({'_id': trailer_id})

    if request.method == 'POST' and 'confirm_delete' in request.form:
        # Eliminar el conductor
        data_manager.delete_conductor(conductor_id)
        flash('Conductor eliminado correctamente', 'success')
        return redirect(url_for('index_conductores'))

    return render_template('conductores/eliminar.html', conductor=conductor, genero=genero, trailer=trailer, generos=generos, trailers=trailers, url_for=url_for)