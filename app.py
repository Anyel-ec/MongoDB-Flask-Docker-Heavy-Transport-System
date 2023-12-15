from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson import ObjectId


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

    # Obtener los datos de la colección "colores"
    colores = {color['_id']: color['nombre'] for color in mongo.db.colores.find()}

    # Combinar los datos de las dos colecciones
    trailers_con_colores = []
    for trailer in trailers:
        color_id = trailer.get('color_id')
        color_nombre = colores.get(color_id, 'Color Desconocido')
        trailer_con_color = {
            'matricula': trailer['matricula'],
            'Ejes': trailer['Ejes'],
            'marca': trailer['marca'],
            'modelo': trailer['modelo'],
            'color': color_nombre,
            'capacidad_carga': trailer['capacidad_carga']
        }
        trailers_con_colores.append(trailer_con_color)

    # Renderizar la plantilla y pasar los datos a la misma
    return render_template('index.html', trailers=trailers_con_colores)




@app.route('/agregar_trailer', methods=['POST'])
def agregar_trailer():
    if request.method == 'POST':
        # Obtener los datos del formulario
        matricula = request.form.get('matricula')
        Ejes = int(request.form.get('Ejes'))
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        color_id = int(request.form.get('color'))  # Obtener el ID del color como entero
        capacidad_carga = int(request.form.get('capacidadCarga'))

        # Crear un nuevo documento para MongoDB con la referencia al color
        nuevo_trailer = {
            'matricula': matricula,
            'Ejes': Ejes,
            'marca': marca,
            'modelo': modelo,
            'color_id': color_id,
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
    # Obtener los colores desde la colección "colores"
    colores = mongo.db.colores.find()
    # Pasar la lista de colores a la plantilla
    return render_template('agregarTrailer.html', colores=colores)



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
    app.run(debug=True, port=5000)

