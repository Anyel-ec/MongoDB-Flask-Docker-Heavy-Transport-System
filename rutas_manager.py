from flask import render_template
from data_manager import DataManager
# importar dependencias
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash


def rutas_home(data_manager):
    rutas = data_manager.get_rutas()
    return render_template('rutas/index.html', rutas=rutas)


def rutas_form(mongo):
    cliente = mongo.db.clientes.find()
    conductor = mongo.db.conductores.find()
    provincia_inicio = mongo.db.provincias.find()
    provincia_fin = mongo.db.provincias.find()

    tipo_carga = mongo.db.tipo_carga.find()
    categoria_carga = mongo.db.categoria_carga.find()
    
    return render_template('rutas/agregar.html', provincia_fin=provincia_fin, conductor=conductor, cliente=cliente, provincia_inicio=provincia_inicio, tipo_carga=tipo_carga, categoria_carga=categoria_carga)

def add_ruta(data_manager):
    cliente_id = request.form.get('cliente')
    conductor_id = request.form.get('conductor')
    provincia_inicio_id = int(request.form.get('provincia_inicio'))
    hora_inicio = request.form.get('fecha_hora_inicio')
    ubicacion_inicio = request.form.get('ubicacion_inicio')
    provincia_fin_id = int(request.form.get('provincia_fin'))
    hora_fin = request.form.get('fecha_hora_fin')
    ubicacion_fin = request.form.get('ubicacion_fin')
    tipo_carga_id = int(request.form.get('tipo_carga'))
    categoria_carga_id = int(request.form.get('categoria_carga'))

    data_manager.add_ruta(cliente_id, conductor_id, provincia_inicio_id, hora_inicio, ubicacion_inicio, provincia_fin_id, hora_fin, ubicacion_fin, tipo_carga_id, categoria_carga_id)
    
    flash('Ruta agregada correctamente', 'success')
    return redirect(url_for('index_rutas'))
