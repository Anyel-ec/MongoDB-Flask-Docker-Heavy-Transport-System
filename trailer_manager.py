from flask import render_template
from data_manager import DataManager
# importar dependencias
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash

def trailer_inicio(data_manager):
    trailers = data_manager.get_trailers()
    return render_template('trailer/index.html', trailers=trailers)

def trailer_form(mongo):
    # Obtener los colores desde la colección "colores"
    colores = mongo.db.colores.find()
    marcas = mongo.db.marcas.find()
    # Pasar la lista de colores a la plantilla
    return render_template('trailer/agregarTrailer.html', colores=colores, marcas=marcas)

def add_trailer(request, data_manager):
    if request.method == 'POST':
        matricula = request.form.get('matricula')

        # Convertir la matrícula a mayúsculas
        matricula = matricula.upper()

        # Verificar si la matrícula ya existe en la colección
        if data_manager.trailer_exists(matricula):
            flash('Ya existe un trailer con esa matrícula', 'danger')
            return redirect(url_for('formulario_agregar_trailer'))
        else:
            Ejes = int(request.form.get('Ejes'))
            marca_id = int(request.form.get('marca'))
            modelo = request.form.get('modelo')
            color_id = int(request.form.get('color'))
            capacidad_carga = int(request.form.get('capacidadCarga'))

            # Intentar agregar el trailer
            if data_manager.add_trailer(matricula, Ejes, marca_id, modelo, color_id, capacidad_carga):
                flash('Error al agregar el trailer', 'danger')
            else:
                flash('Trailer agregado correctamente', 'success')

    # Redirigir al índice solo si el trailer se agregó correctamente
    return redirect(url_for('index'))

    
def update_trailer(mongo, data_manager, trailer_id):
    trailer = mongo.db.trailer.find_one({'_id': ObjectId(trailer_id)})
    if request.method == 'POST':
        nueva_matricula = request.form.get('matricula')

        # Verificar si la nueva matrícula ya existe en otro trailer
        if nueva_matricula != trailer['matricula'] and data_manager.trailer_exists(nueva_matricula):
            flash('Ya existe un trailer con esa matrícula', 'danger')
            return redirect(url_for('editar_trailer', trailer_id=trailer_id))

        nuevo_modelo = request.form.get('modelo')
        nuevo_color_id = int(request.form.get('color'))
        nueva_capacidad_carga = int(request.form.get('capacidadCarga'))
        nuevo_marca_id = int(request.form.get('marca'))
        nuevo_ejes_id = int(request.form.get('Ejes'))
        
        data_manager.edit_trailer_by_id(trailer_id, nueva_matricula, nuevo_modelo, nuevo_color_id, nueva_capacidad_carga, nuevo_marca_id, nuevo_ejes_id)
        flash('Trailer actualizado correctamente', 'success')
        return redirect(url_for('index'))

    colores = mongo.db.colores.find()
    marcas = mongo.db.marcas.find()

    return render_template('trailer/actualizarTrailer.html', trailer=trailer, colores=colores, marcas=marcas)

# Eliminar
def delete_trailer(trailer_id, mongo, data_manager):
    marcas = mongo.db.marcas.find()
    colores = mongo.db.colores.find()
    trailer = mongo.db.trailer.find_one({'_id': ObjectId(trailer_id)})
    
    # Obtener información de la marca y el color utilizando sus IDs en el trailer
    marca_id = trailer.get('marca_id')
    color_id = trailer.get('color_id')
    
    marca = mongo.db.marcas.find_one({'_id': marca_id})
    color = mongo.db.colores.find_one({'_id': color_id})
    
    if request.method == 'POST' and 'confirm_delete' in request.form:
        # Eliminar el trailer
        data_manager.delete_trailer(trailer_id)
        flash('Trailer eliminado correctamente', 'success')
        return redirect(url_for('index'))
    return render_template('trailer/eliminarTrailer.html', trailer=trailer, marca=marca, color=color, marcas=marcas, colores=colores, url_for=url_for)

