import os
from pymongo import MongoClient
from dotenv import load_dotenv


def migrar_datos():

    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener la URI de MongoDB y la clave secreta desde las variables de entorno
    mongo_uri = os.getenv('MONGO_URI')
    secret_key = os.getenv('SECRET_KEY')

    # Conexión a la base de datos MongoDB
    client = MongoClient(mongo_uri)
    # Utiliza la base de datos predeterminada de la URI
    db = client.get_default_database()

    # JSON de datos
    data = [
        {"_id": 1, "nombre": "Carga Frágil"},
        {"_id": 2, "nombre": "Carga No Frágil"},
        {"_id": 3, "nombre": "Carga Moderadamente Frágil"},
        {"_id": 4, "nombre": "Carga Peligrosa"},
        {"_id": 5, "nombre": "Carga Perecedera"},
        {"_id": 6, "nombre": "Carga Química"},
        {"_id": 7, "nombre": "Carga Voluminosa"},
        {"_id": 8, "nombre": "Carga Sólida a Granel"},
        {"_id": 9, "nombre": "Carga Líquida a Granel"},
        {"_id": 10, "nombre": "Carga Refrigerada"},
        {"_id": 11, "nombre": "Carga Sensible a la Temperatura"},
        {"_id": 12, "nombre": "Carga Perecedera"},
        {"_id": 13, "nombre": "Carga Seca"},
        {"_id": 14, "nombre": "Carga Especializada"},
        {"_id": 15, "nombre": "Carga de Maquinaria Pesada"}
    ]

    # Colección en MongoDB
    collection = db['categoria_carga']

    # Operación replace_many
    for record in data:
        # Utilizamos upsert=True para que si no existe, se cree
        collection.replace_one({"_id": record["_id"]}, record, upsert=True)

    # JSON de datos de colores
    colores_data = [
        {"_id": 1, "nombre": "Rojo"},
        {"_id": 2, "nombre": "Verde"},
        {"_id": 3, "nombre": "Azul"},
        {"_id": 4, "nombre": "Amarillo"},
        {"_id": 5, "nombre": "Naranja"},
        {"_id": 6, "nombre": "Morado"},
        {"_id": 7, "nombre": "Rosa"},
        {"_id": 8, "nombre": "Gris"},
        {"_id": 9, "nombre": "Blanco"},
        {"_id": 10, "nombre": "Negro"}
    ]

    # Colección en MongoDB para colores
    colores_collection = db['colores']

    # Operación replace_many para colores
    for color_record in colores_data:
        # Utilizamos upsert=True para que si no existe, se cree
        colores_collection.replace_one(
            {"_id": color_record["_id"]}, color_record, upsert=True)

    # JSON de datos de géneros
    generos_data = [
        {"_id": 1, "nombre": "Masculino"},
        {"_id": 2, "nombre": "Femenino"}
    ]

    # Colección en MongoDB para géneros
    generos_collection = db['genero']

    # Operación replace_many para géneros
    for genero_record in generos_data:
        # Utilizamos upsert=True para que si no existe, se cree
        generos_collection.replace_one(
            {"_id": genero_record["_id"]}, genero_record, upsert=True)

    marcas_data = [
        {"_id": 1, "nombre": "JAC"},
        {"_id": 2, "nombre": "Nissan"},
        {"_id": 3, "nombre": "Toyota"},
        {"_id": 4, "nombre": "Chevrolet"},
        {"_id": 5, "nombre": "Fontaine"},
        {"_id": 6, "nombre": "Pitts"},
        {"_id": 7, "nombre": "Reitnouer"},
        {"_id": 8, "nombre": "Mac Trailer"},
        {"_id": 9, "nombre": "Stoughton"},
        {"_id": 10, "nombre": "Transcraft"},
        {"_id": 11, "nombre": "East"},
        {"_id": 12, "nombre": "Dorsey"},
        {"_id": 13, "nombre": "Wilson"},
        {"_id": 14, "nombre": "Manac"},
        {"_id": 15, "nombre": "Vanguard"},
        {"_id": 16, "nombre": "Hyundai"},
        {"_id": 17, "nombre": "XL Specialized"},
        {"_id": 18, "nombre": "Polar Tank"},
        {"_id": 19, "nombre": "Kalyn Siebert"},
        {"_id": 20, "nombre": "Doonan Specialized, LLC"}
    ]

    # Colección en MongoDB para marcas
    marcas_collection = db['marcas']

    # Operación replace_many para marcas
    for marca_record in marcas_data:
        # Utilizamos upsert=True para que si no existe, se cree
        marcas_collection.replace_one(
            {"_id": marca_record["_id"]}, marca_record, upsert=True)

    # JSON de datos de provincias
    provincias_data = [
        {"_id": 1, "nombre": "Azuay"},
        {"_id": 2, "nombre": "Bolívar"},
        {"_id": 3, "nombre": "Cañar"},
        {"_id": 4, "nombre": "Carchi"},
        {"_id": 5, "nombre": "Chimborazo"},
        {"_id": 6, "nombre": "Cotopaxi"},
        {"_id": 7, "nombre": "El Oro"},
        {"_id": 8, "nombre": "Esmeraldas"},
        {"_id": 9, "nombre": "Galápagos"},
        {"_id": 10, "nombre": "Guayas"},
        {"_id": 11, "nombre": "Imbabura"},
        {"_id": 12, "nombre": "Loja"},
        {"_id": 13, "nombre": "Los Ríos"},
        {"_id": 14, "nombre": "Manabí"},
        {"_id": 15, "nombre": "Morona Santiago"},
        {"_id": 16, "nombre": "Napo"},
        {"_id": 17, "nombre": "Orellana"},
        {"_id": 18, "nombre": "Pastaza"},
        {"_id": 19, "nombre": "Pichincha"},
        {"_id": 20, "nombre": "Santa Elena"},
        {"_id": 21, "nombre": "Santo Domingo de los Tsáchilas"},
        {"_id": 22, "nombre": "Sucumbíos"},
        {"_id": 23, "nombre": "Tungurahua"},
        {"_id": 24, "nombre": "Zamora-Chinchipe"}
    ]

    # Colección en MongoDB para provincias
    provincias_collection = db['provincias']

    for provincia_record in provincias_data:
        # Utilizamos upsert=True para que si no existe, se cree
        provincias_collection.replace_one(
            {"_id": provincia_record["_id"]}, provincia_record, upsert=True)

    # JSON de datos de tipo_carga
    tipo_carga_data = [
        {"_id": 1, "nombre": "Productos Electrónicos"},
        {"_id": 2, "nombre": "Alimentos Perecederos"},
        {"_id": 3, "nombre": "Productos Químicos"},
        {"_id": 4, "nombre": "Materiales de Construcción"},
        {"_id": 5, "nombre": "Automóviles y Vehículos"},
        {"_id": 6, "nombre": "Ropa y Textiles"},
        {"_id": 7, "nombre": "Productos Farmacéuticos"},
        {"_id": 8, "nombre": "Madera y Productos Forestales"},
        {"_id": 9, "nombre": "Productos a Granel Secos"},
        {"_id": 10, "nombre": "Equipos Industriales"},
        {"_id": 11, "nombre": "Carga General"},
        {"_id": 12, "nombre": "Contenedores Intermodales"},
        {"_id": 13, "nombre": "Productos de Consumo"},
        {"_id": 14, "nombre": "Productos Metalúrgicos"},
        {"_id": 15, "nombre": "Productos de Papel y Cartón"}
    ]

    # Colección en MongoDB para tipo_carga
    tipo_carga_collection = db['tipo_carga']

    # Operación replace_many para tipo_carga
    for tipo_carga_record in tipo_carga_data:
        # Utilizamos upsert=True para que si no existe, se cree
        tipo_carga_collection.replace_one(
            {"_id": tipo_carga_record["_id"]}, tipo_carga_record, upsert=True)

    # Cierra la conexión
    client.close()
