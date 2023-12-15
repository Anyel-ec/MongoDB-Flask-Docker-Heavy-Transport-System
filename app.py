from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configuración de la base de datos MongoDB desde la variable de entorno
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def index():
    # Obtener los datos de la colección "trailer"
    trailers = mongo.db.trailer.find()
    # Renderizar la plantilla y pasar los datos a la misma
    return render_template('index.html', trailers=trailers)

@app.route('/agregar_trailer', methods=['POST'])
def agregar_trailer():
    if request.method == 'POST':
        # Obtener los datos del formulario
        matricula = request.form.get('matricula')
        Ejes = int(request.form.get('Ejes'))
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        color = request.form.get('color')
        capacidad_carga = int(request.form.get('capacidadCarga'))

        # Crear un nuevo documento para MongoDB
        nuevo_trailer = {
            'matricula': matricula,
            'Ejes': Ejes,
            'marca': marca,
            'modelo': modelo,
            'color': color,
            'capacidad_carga': capacidad_carga
        }

        # Insertar el nuevo trailer en la colección "trailer"
        mongo.db.trailer.insert_one(nuevo_trailer)
        flash('Trailer agregado correctamente', 'success')
        # Redirigir a la página principal después de agregar el trailer
        return redirect(url_for('index'))
    


# Nueva ruta para renderizar la plantilla agregarTrailer.html
@app.route('/formulario_agregar_trailer')
def formulario_agregar_trailer():
    return render_template('agregarTrailer.html')


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
    app.run(debug=True, port=5001)

