from pymongo import MongoClient


def get_mongo_connection():
    try:
        # Configuración de conexión
        MONGODB_SETTINGS = {
            'host': 'mongodb://localhost:27017/prueba'
        }

        # Crear una instancia del cliente de MongoDB
        client = MongoClient(MONGODB_SETTINGS['host'])

        # Seleccionar una base de datos (puede ser cualquier base de datos para probar la conexión)
        db = client.get_database()

        # Devolver el cliente y la base de datos
        return client, db

    except Exception as e:
        # Si hay un error, imprimir el mensaje de error
        print(f"Error de conexión a la base de datos: {e}")
        return None, None


def close_mongo_connection(client):
    # Cerrar la conexión
    if client:
        client.close()

# Puedes agregar otras configuraciones aquí si es necesario
