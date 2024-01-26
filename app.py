from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson import ObjectId
from data_manager import DataManager
from trailer_manager import trailer_inicio, trailer_form, add_trailer, update_trailer, delete_trailer
from clientes_manager import clientes_home, cliente_form, add_cliente, update_cliente, delete_cliente
from conductores_manager import conductores_home, conductor_form, add_conductor, update_conductor, delete_conductor
from rutas_manager import rutas_home, rutas_form, add_ruta, update_ruta, delete_ruta
from migration import migrar_datos

#Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)


# Cargar variables de entorno desde el archivo .env
app.secret_key = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
data_manager = DataManager(mongo)
migrar_datos()
#######################################################################################################################
# Rutas del Trailer 
@app.route('/')
def index():
    return trailer_inicio(data_manager)

@app.route('/formulario')
def formulario_agregar_trailer():
    return trailer_form(mongo)

@app.route('/agregar', methods=['POST'])
def agregar_trailer():
    return add_trailer(request, data_manager)

@app.route('/editar/<string:trailer_id>', methods=['GET', 'POST'])
def editar_trailer(trailer_id):
    return update_trailer(mongo, data_manager, trailer_id)

@app.route('/eliminar/<string:trailer_id>', methods=['GET', 'POST'])
def eliminar_trailer(trailer_id):
    return delete_trailer(trailer_id, mongo, data_manager)

#######################################################################################################################

# Rutas del Cliente
@app.route('/cliente/')
def index_clientes():
    return clientes_home(data_manager)

# Nueva ruta para renderizar la plantilla agregarTrailer.html
@app.route('/cliente/formulario')
def formulario_agregar_cliente():
    return cliente_form(mongo)

@app.route('/cliente/agregar', methods=['POST'])
def agregar_cliente():
    return add_cliente(request, data_manager)
    

@app.route('/cliente/editar/<string:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    return update_cliente(mongo, cliente_id, data_manager)

@app.route('/cliente/eliminar/<string:cliente_id>', methods=['GET', 'POST'])
def eliminar_cliente(cliente_id):
    return delete_cliente(cliente_id, mongo, data_manager)

#######################################################################################################################
# Rutas del Conductor
@app.route('/conductor/')
def index_conductores():
    return conductores_home(data_manager)

@app.route('/conductor/formulario')
def formulario_agregar_conductor():
    return conductor_form(mongo)

@app.route('/conductor/agregar', methods=['POST'])
def agregar_conductor():
    return add_conductor(request, data_manager)
    
@app.route('/conductor/editar/<string:conductor_id>', methods=['GET', 'POST'])
def editar_conductor(conductor_id):
    return update_conductor(mongo, conductor_id, data_manager)

@app.route('/conductor/eliminar/<string:conductor_id>', methods=['GET', 'POST'])
def eliminar_conductor(conductor_id):
    return delete_conductor(conductor_id, mongo, data_manager)

#######################################################################################################################
# Ruta del Rutas

@app.route('/rutas/')
def index_rutas():
    return rutas_home(data_manager)

@app.route('/rutas/formulario')
def formulario_agregar_rutas():
    return rutas_form(mongo)

@app.route('/rutas/agregar', methods=['POST'])
def agregar_ruta():
    return add_ruta(data_manager)

@app.route('/rutas/editar/<string:ruta_id>', methods=['GET', 'POST'])
def editar_ruta(ruta_id):
    return update_ruta(mongo, ruta_id, data_manager)

@app.route('/rutas/eliminar/<string:ruta_id>', methods=['GET', 'POST'])
def eliminar_ruta(ruta_id):
    return delete_ruta(ruta_id, mongo, data_manager)


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
    #aceptar todas las redes
    app.run(port=5001, debug=True, host='0.0.0.0')

