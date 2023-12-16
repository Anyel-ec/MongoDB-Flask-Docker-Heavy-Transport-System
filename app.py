from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson import ObjectId
from data_manager import DataManager

#Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Cargar variables de entorno desde el archivo .env

app.secret_key = os.getenv('SECRET_KEY')

# Configuración de la base de datos MongoDB desde la variable de entorno
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

data_manager = DataManager(mongo)


@app.route('/')
def index():
    trailers_con_colores = data_manager.get_trailers_with_colors()
    return render_template('trailer/index.html', trailers=trailers_con_colores)

# Nueva ruta para renderizar la plantilla agregarTrailer.html
@app.route('/formulario_agregar_trailer')
def formulario_agregar_trailer():
    # Obtener los colores desde la colección "colores"
    colores = mongo.db.colores.find()
    marcas = mongo.db.marcas.find()

    # Pasar la lista de colores a la plantilla
    return render_template('trailer/agregarTrailer.html', colores=colores, marcas=marcas)

@app.route('/agregar_trailer', methods=['POST'])
def agregar_trailer():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        Ejes = int(request.form.get('Ejes'))
        marca_id = int(request.form.get('marca'))
        modelo = request.form.get('modelo')
        color_id = int(request.form.get('color'))
        capacidad_carga = int(request.form.get('capacidadCarga'))

        data_manager.add_trailer(matricula, Ejes, marca_id, modelo, color_id, capacidad_carga)

        flash('Trailer agregado correctamente', 'success')
        return redirect(url_for('index'))

# En app.py
@app.route('/editar_trailer/<string:trailer_id>', methods=['GET', 'POST'])
def editar_trailer(trailer_id):
    trailer = mongo.db.trailer.find_one({'_id': ObjectId(trailer_id)})

    if request.method == 'POST':
        nueva_matricula = request.form.get('matricula')
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



@app.route('/eliminar_trailer/<string:trailer_id>', methods=['GET', 'POST'])
def eliminar_trailer(trailer_id):

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


# Ruta de ejemplo para probar la conexión
@app.route('/test_mongo_connection')
def test_mongo_connection():
    try:
        # Intenta realizar una consulta simple para verificar la conexión
        result = mongo.db.test_collection.find_one()
        return jsonify({'message': 'Conexión exitosa a MongoDB', 'data': result})
    except Exception as e:
        return jsonify({'message': 'Error en la conexión a MongoDB', 'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

