from flask import Flask, jsonify, request
from config import get_mongo_connection, close_mongo_connection

app = Flask(__name__)

# Ruta para insertar datos en la colección 'persona'
@app.route('/insertar_persona', methods=['POST'])
def insertar_persona():
    try:
        # Obtener la conexión a la base de datos
        mongo_client, mongo_db = get_mongo_connection()

        # Verificar si hay conexión
        if mongo_client and mongo_db:
            # Obtener la colección 'persona'
            persona_collection = mongo_db.get_collection('persona')

            # Obtener los datos del cuerpo de la solicitud POST
            data = request.json

            # Insertar los datos en la colección 'persona'
            result = persona_collection.insert_one(data)

            # Imprimir el ID del documento insertado
            print(f"Documento insertado con ID: {result.inserted_id}")

            return jsonify({'status': 'success', 'message': 'Datos insertados correctamente'})

        else:
            return jsonify({'status': 'error', 'message': 'No hay conexión a la base de datos'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al insertar datos: {e}'})

    finally:
        # Cerrar la conexión después de realizar las operaciones necesarias
        close_mongo_connection(mongo_client)

# Puedes agregar más rutas y funcionalidades aquí

if __name__ == '__main__':
    app.run(debug=True)
