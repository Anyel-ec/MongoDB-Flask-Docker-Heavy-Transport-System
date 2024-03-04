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
    consumo = request.form.get('consumo')
    precio = request.form.get('precio')
    paradas = request.form.get('paradas')
    data_manager.add_ruta(cliente_id, conductor_id, provincia_inicio_id, hora_inicio, ubicacion_inicio, provincia_fin_id, hora_fin, ubicacion_fin, tipo_carga_id, categoria_carga_id, consumo, precio, paradas)
    
    flash('Ruta agregada correctamente', 'success')
    return redirect(url_for('index_rutas'))

def update_ruta(mongo, ruta_id, data_manager):
    ruta = mongo.db.rutas.find_one({'_id': ObjectId(ruta_id)})

    if request.method == 'POST':
        # Obtén los datos actualizados del formulario y actualiza la ruta
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

        consumo = request.form.get('consumo')
        precio = request.form.get('precio')
        paradas = request.form.get('paradas')

        data_manager.edit_ruta_by_id(
            ruta_id, cliente_id, conductor_id, provincia_inicio_id,
            hora_inicio, ubicacion_inicio, provincia_fin_id, hora_fin,
            ubicacion_fin, tipo_carga_id, categoria_carga_id, consumo, precio, paradas
        )
        
        flash('Ruta actualizada correctamente', 'success')
        return redirect(url_for('index_rutas'))

    clientes = mongo.db.clientes.find()
    conductores = mongo.db.conductores.find()
    provincia_inicio = mongo.db.provincias.find()
    provincia_fin = mongo.db.provincias.find()
    tipos_carga = mongo.db.tipo_carga.find()
    categorias_carga = mongo.db.categoria_carga.find()


    return render_template(
        'rutas/actualizar.html', ruta=ruta, clientes=clientes,
        conductores=conductores, provincia_inicio=provincia_inicio,
        provincia_fin=provincia_fin,
        tipos_carga=tipos_carga, categorias_carga=categorias_carga
    )

def delete_ruta(ruta_id, mongo, data_manager):
    clientes = mongo.db.clientes.find()
    conductores = mongo.db.conductores.find()
    provincias = mongo.db.provincias.find()
    tipos_carga = mongo.db.tipo_carga.find()
    categorias_carga = mongo.db.categoria_carga.find()

    ruta = mongo.db.rutas.find_one({'_id': ObjectId(ruta_id)})
    cliente_id = str(ruta.get('cliente'))
    conductor_id = str(ruta.get('conductor_responsable'))
    provincia_inicio_id = ruta.get('provincia_inicio')
    provincia_fin_id = ruta.get('provincia_fin')
    tipo_carga_id = ruta.get('tipos_carga')
    categoria_carga_id = ruta.get('categoria_carga')
    consumo = ruta.get('consumo')
    precio = ruta.get('precio')
    paradas = ruta.get('paradas')
    cliente = mongo.db.clientes.find_one({'_id': ObjectId(cliente_id)})
    
    conductor = mongo.db.conductores.find_one({'_id': ObjectId(conductor_id)})
    provincia_inicio = mongo.db.provincias.find_one({'_id': provincia_inicio_id})
    provincia_final = mongo.db.provincias.find_one({'_id': (provincia_fin_id)})
    tipo_carga = mongo.db.tipo_carga.find_one({'_id': (tipo_carga_id)})
    categoria_carga = mongo.db.categoria_carga.find_one({'_id': (categoria_carga_id)})

    if request.method == 'POST' and 'confirm_delete' in request.form:
        # Eliminar la ruta
        data_manager.delete_ruta(ruta_id)
        flash('Ruta eliminada correctamente', 'success')
        return redirect(url_for('index_rutas'))

    return render_template('rutas/eliminar.html', ruta=ruta, cliente=cliente, conductor=conductor,
                           provincia_inicio=provincia_inicio, provincia_final=provincia_final, tipo_carga=tipo_carga,
                           categoria_carga=categoria_carga, clientes=clientes, conductores=conductores,
                           provincias=provincias, tipos_carga=tipos_carga, categorias_carga=categorias_carga, consumo=consumo, precio=precio, paradas=paradas,
                           url_for=url_for)

