from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos MongoDB desde la variable de entorno
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def index():
    # Obtener los datos de la colección "trailer"
    trailers = mongo.db.trailer.find()

    # Renderizar la plantilla y pasar los datos a la misma
    return render_template('index.html', trailers=trailers)


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
    app.run(debug=True)
