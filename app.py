from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson import ObjectId
from data_manager import DataManager
from trailer_manager import trailer_inicio, trailer_form, add_trailer, update_trailer, delete_trailer
from clientes_manager import clientes_home, cliente_form, add_cliente, update_cliente, delete_cliente
#Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Cargar variables de entorno desde el archivo .env
app.secret_key = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
data_manager = DataManager(mongo)


# Rutas del Trailer 
@app.route('/')
def index():
    return trailer_inicio(data_manager)

@app.route('/formulario_agregar_trailer')
def formulario_agregar_trailer():
    return trailer_form(mongo)

@app.route('/agregar_trailer', methods=['POST'])
def agregar_trailer():
    return add_trailer(request, data_manager)

@app.route('/editar_trailer/<string:trailer_id>', methods=['GET', 'POST'])
def editar_trailer(trailer_id):
    return update_trailer(mongo, data_manager, trailer_id)

@app.route('/eliminar_trailer/<string:trailer_id>', methods=['GET', 'POST'])
def eliminar_trailer(trailer_id):
    return delete_trailer(trailer_id, mongo, data_manager)




@app.route('/clientes/')
def index_clientes():
    return clientes_home(data_manager)

# Nueva ruta para renderizar la plantilla agregarTrailer.html
@app.route('/clientes/formulario_agregar_cliente')
def formulario_agregar_cliente():
    return cliente_form(mongo)

@app.route('/clientes/agregar_cliente', methods=['POST'])
def agregar_cliente():
    return add_cliente(data_manager)
    

@app.route('/clientes/editar_cliente/<string:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    return update_cliente(mongo, cliente_id, data_manager)

@app.route('/clientes/eliminar_cliente/<string:cliente_id>', methods=['GET', 'POST'])
def eliminar_cliente(cliente_id):
    return delete_cliente(cliente_id, mongo, data_manager)



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

