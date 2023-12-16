# data_manager.py
from flask_pymongo import PyMongo

class DataManager:
    def __init__(self, mongo):
        self.mongo = mongo

    def get_trailers_with_colors(self):
        trailers = self.mongo.db.trailer.find()
        colores = {color['_id']: color['nombre'] for color in self.mongo.db.colores.find()}
        marcas = {marca['_id']: marca['nombre'] for marca in self.mongo.db.marcas.find()}
        trailers_con_colores = []

        for trailer in trailers:
            color_id = trailer.get('color_id')
            color_nombre = colores.get(color_id, 'Color Desconocido')
            marca_id = trailer.get('marca_id')
            marca_nombre = marcas.get(marca_id, 'Marca Desconocida')
            trailer_con_color = {
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
    
    def edit_trailer(self, matricula, nuevo_modelo, nuevo_color_id, nueva_capacidad_carga):
        self.mongo.db.trailer.update_one(
            {'matricula': matricula},
            {'$set': {
                'modelo': nuevo_modelo,
                'color_id': nuevo_color_id,
                'capacidad_carga': nueva_capacidad_carga
            }}
        )
        
    def delete_trailer(self, matricula):
        trailer = self.mongo.db.trailer.find_one({'matricula': matricula})

        if trailer:
            marca = self.mongo.db.marcas.find_one({'_id': trailer['marca_id']})
            color = self.mongo.db.colores.find_one({'_id': trailer['color_id']})
        else:
            marca = None
            color = None

        if trailer:
            self.mongo.db.trailer.delete_one({'matricula': matricula})

        return trailer, marca, color
