from flask_pymongo import PyMongo
from bson import ObjectId


class DataManager:
    def __init__(self, mongo):
        self.mongo = mongo

    def get_trailers(self):
        trailers = self.mongo.db.trailer.find()
        colores = {color['_id']: color['nombre']
                   for color in self.mongo.db.colores.find()}
        marcas = {marca['_id']: marca['nombre']
                  for marca in self.mongo.db.marcas.find()}
        trailers_con_colores = []

        for trailer in trailers:
            color_id = trailer.get('color_id')
            color_nombre = colores.get(color_id, 'Color Desconocido')
            marca_id = trailer.get('marca_id')
            marca_nombre = marcas.get(marca_id, 'Marca Desconocida')
            trailer_con_color = {
                '_id': str(trailer['_id']),
                'matricula': trailer['matricula'],
                'Ejes': trailer['Ejes'],
                'marca': marca_nombre,
                'modelo': trailer['modelo'],
                'color': color_nombre,
                'capacidad_carga': trailer['capacidad_carga']
            }
            trailers_con_colores.append(trailer_con_color)

        return trailers_con_colores

    def add_trailer(self, matricula, Ejes, marca_id, modelo, color_id, capacidad_carga):
        nuevo_trailer = {
            'matricula': matricula,
            'Ejes': Ejes,
            'marca_id': marca_id,
            'modelo': modelo,
            'color_id': color_id,
            'capacidad_carga': capacidad_carga
        }

        self.mongo.db.trailer.insert_one(nuevo_trailer)

    def edit_trailer_by_id(self, trailer_id, nueva_matricula, nuevo_modelo, nuevo_color_id, nueva_capacidad_carga, nuevo_marca_id, nuevo_ejes_id):
        self.mongo.db.trailer.update_one(
            {'_id': ObjectId(trailer_id)},
            {'$set': {
                'matricula': nueva_matricula,
                'modelo': nuevo_modelo,
                'color_id': nuevo_color_id,
                'capacidad_carga': nueva_capacidad_carga,
                'marca_id': nuevo_marca_id,
                'Ejes': nuevo_ejes_id
            }}
        )

    def delete_trailer(self, trailer_id):
        trailer = self.mongo.db.trailer.find_one({'_id': ObjectId(trailer_id)})

        if trailer:
            marca = self.mongo.db.marcas.find_one({'_id': trailer['marca_id']})
            color = self.mongo.db.colores.find_one(
                {'_id': trailer['color_id']})
        else:
            marca = None
            color = None

        if trailer:
            self.mongo.db.trailer.delete_one({'_id': ObjectId(trailer_id)})

        return trailer, marca, color

    # CLIENTES
    def get_clientes(self):
        clientes = self.mongo.db.clientes.find()
        generos = {genero['_id']: genero['nombre']
                for genero in self.mongo.db.genero.find()}
        provincias = {provincia['_id']: provincia['nombre']
                    for provincia in self.mongo.db.provincias.find()}
        clientes_con_datos = []

        for cliente in clientes:
            genero_id = cliente.get('genero_id')
            genero_nombre = generos.get(genero_id, 'Género Desconocido')
            provincia_id = cliente.get('provincia_id')
            provincia_nombre = provincias.get(provincia_id, 'Provincia Desconocida')
            cliente_con_datos = {
                '_id': str(cliente['_id']),
                'nombres': cliente['nombres'],
                'cedula': cliente['cedula'],
                'correo': cliente['correo'],
                'direccion': cliente['direccion'],
                'provincia': provincia_nombre,
                'genero': genero_nombre,
            }
            clientes_con_datos.append(cliente_con_datos)

        return clientes_con_datos

    
    # En data_manager.py
    def add_cliente(self, nombres, cedula, correo, direccion, provincia_id, genero_id):
        nuevo_cliente = {
            'nombres': nombres,
            'cedula': cedula,
            'correo': correo,
            'direccion': direccion,
            'provincia_id': provincia_id,
            'genero_id': genero_id,
        }

        self.mongo.db.clientes.insert_one(nuevo_cliente)

    def edit_cliente_by_id(self, cliente_id, nuevo_nombres, nueva_cedula, nuevo_correo, nueva_direccion, nueva_provincia_id, nuevo_genero_id):
        self.mongo.db.clientes.update_one(
            {'_id': ObjectId(cliente_id)},
            {'$set': {
                'nombres': nuevo_nombres,
                'cedula': nueva_cedula,
                'correo': nuevo_correo,
                'direccion': nueva_direccion,
                'provincia_id': nueva_provincia_id,
                'genero_id': nuevo_genero_id
            }}
        )
        
    def delete_cliente(self, cliente_id):
        cliente = self.mongo.db.clientes.find_one({'_id': ObjectId(cliente_id)})

        if cliente:
            provincia = self.mongo.db.provincias.find_one(
                {'_id': cliente['provincia_id']})
            genero = self.mongo.db.genero.find_one(
                {'_id': cliente['genero_id']})
        else:
            provincia = None
            genero = None

        if cliente:
            self.mongo.db.clientes.delete_one({'_id': ObjectId(cliente_id)})

        return cliente, provincia, genero