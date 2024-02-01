from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime


class DataManager:
    def __init__(self, mongo):
        self.mongo = mongo
    def get_trailers(self):
        # Filtrar los trailers eliminados (eliminado=False)
        trailers = self.mongo.db.trailer.find({'eliminado': False})
        colores = {color['_id']: color['nombre'] for color in self.mongo.db.colores.find()}
        marcas = {marca['_id']: marca['nombre'] for marca in self.mongo.db.marcas.find()}
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
        existing_trailer = self.mongo.db.trailer.find_one({'matricula': matricula})

        if existing_trailer:
            self.mongo.db.trailer.update_one(
                {'_id': existing_trailer['_id']},
                {'$set': {
                    'Ejes': Ejes,
                    'marca_id': marca_id,
                    'modelo': modelo,
                    'color_id': color_id,
                    'capacidad_carga': capacidad_carga,
                    'eliminado': False
                }}
            )
            return 'Trailer actualizado correctamente'
        else:
            nuevo_trailer = {
                'matricula': matricula,
                'Ejes': Ejes,
                'marca_id': marca_id,
                'modelo': modelo,
                'color_id': color_id,
                'capacidad_carga': capacidad_carga,
                'eliminado': False
            }
            self.mongo.db.trailer.insert_one(nuevo_trailer)
            return 'Trailer agregado correctamente'
    
    def trailer_exists(self, matricula):
            existing_trailer = self.mongo.db.trailer.find_one({'matricula': matricula})
            return existing_trailer is not None
    
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
            color = self.mongo.db.colores.find_one({'_id': trailer['color_id']})
        else:
            marca = None
            color = None

        if trailer:
            # Actualizar el campo "eliminado" en lugar de eliminar físicamente
            self.mongo.db.trailer.update_one({'_id': ObjectId(trailer_id)},
                                             {'$set': {'eliminado': True}})
        return trailer, marca, color
#########################################################################################################################
    # CLIENTES

    def get_clientes(self):
        clientes = self.mongo.db.clientes.find({'eliminado': False})
        generos = {genero['_id']: genero['nombre'] for genero in self.mongo.db.genero.find()}
        provincias = {provincia['_id']: provincia['nombre'] for provincia in self.mongo.db.provincias.find()}
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

    def add_cliente(self, nombres, cedula, correo, direccion, provincia_id, genero_id):
        existing_cliente = self.mongo.db.clientes.find_one({'cedula': cedula})

        if existing_cliente:
            self.mongo.db.clientes.update_one(
                {'_id': existing_cliente['_id']},
                {'$set': {
                    'nombres': nombres,
                    'correo': correo,
                    'direccion': direccion,
                    'provincia_id': provincia_id,
                    'genero_id': genero_id,
                    'eliminado': False
                }}
            )
            return 'Cliente actualizado correctamente'
        else:
            nuevo_cliente = {
                'nombres': nombres,
                'cedula': cedula,
                'correo': correo,
                'direccion': direccion,
                'provincia_id': provincia_id,
                'genero_id': genero_id,
                'eliminado': False
            }
            self.mongo.db.clientes.insert_one(nuevo_cliente)
            return 'Cliente agregado correctamente'

    def cliente_exists(self, cedula):
        existing_cliente = self.mongo.db.clientes.find_one({'cedula': cedula})
        return existing_cliente is not None

    def edit_cliente_by_id(self, cliente_id, nuevo_nombres, nueva_cedula, nuevo_correo, nueva_direccion, nueva_provincia_id, nuevo_genero_id):
        self.mongo.db.clientes.update_one(
            {'_id': ObjectId(cliente_id)},
            {'$set': {
                'nombres': nuevo_nombres,
                'cedula': nueva_cedula,
                'correo': nuevo_correo,
                'direccion': nueva_direccion,
                'provincia_id': nueva_provincia_id,
                'genero_id': nuevo_genero_id,
                'eliminado': False
            }}
        )

    def delete_cliente(self, cliente_id):
        cliente = self.mongo.db.clientes.find_one({'_id': ObjectId(cliente_id)})

        if cliente:
            provincia = self.mongo.db.provincias.find_one({'_id': cliente['provincia_id']})
            genero = self.mongo.db.genero.find_one({'_id': cliente['genero_id']})
        else:
            provincia = None
            genero = None

        if cliente:
            self.mongo.db.clientes.update_one({'_id': ObjectId(cliente_id)}, {'$set': {'eliminado': True}})

        return cliente, provincia, genero

#########################################################################################################################
    # CONDUCTORES
    def get_conductores(self):
        conductores = self.mongo.db.conductores.find({'eliminado': False})
        generos = {genero['_id']: genero['nombre'] for genero in self.mongo.db.genero.find()}
        trailers = {trailer['_id']: trailer['matricula'] for trailer in self.mongo.db.trailer.find()}
        conductores_con_info = []

        for conductor in conductores:
            genero_id = conductor.get('genero_id')
            genero_nombre = generos.get(genero_id, 'Género Desconocido')
            trailer_id = conductor.get('trailer_id')
            trailer_matricula = trailers.get(trailer_id, 'Trailer Desconocido')

            conductor_con_info = {
                '_id': str(conductor['_id']),
                'nombre': conductor['nombre'],
                'telefono': conductor['telefono'],
                'fecha_nacimiento': conductor['fecha_nacimiento'],
                'correo': conductor['correo'],
                'genero': genero_nombre,
                'cedula': conductor['cedula'],
                'trailer_matricula': trailer_matricula
            }

            conductores_con_info.append(conductor_con_info)

        return conductores_con_info

    def add_conductor(self, nombres, cedula, telefono, fecha_nacimiento, correo, genero_id, trailer_id):
        # Buscar si ya existe un conductor con la misma cédula
        existing_conductor = self.mongo.db.conductores.find_one({'cedula': cedula})

        if existing_conductor:
            # Si existe, actualizar los valores y establecer eliminado en False
            self.mongo.db.conductores.update_one(
                {'_id': existing_conductor['_id']},
                {'$set': {
                    'nombre': nombres,
                    'telefono': telefono,
                    'fecha_nacimiento': fecha_nacimiento,
                    'correo': correo,
                    'genero_id': genero_id,
                    'trailer_id': ObjectId(trailer_id),
                    'eliminado': False
                }}
            )
            return 'Conductor actualizado correctamente'
        else:
            # Si no existe, agregar un nuevo conductor
            nuevo_conductor = {
                'nombre': nombres,
                'cedula': cedula,
                'telefono': telefono,
                'fecha_nacimiento': fecha_nacimiento,
                'correo': correo,
                'genero_id': genero_id,
                'trailer_id': ObjectId(trailer_id),
                'eliminado': False
            }
            self.mongo.db.conductores.insert_one(nuevo_conductor)
            return 'Conductor agregado correctamente'



    def conductor_exists(self, cedula):
        existing_conductor = self.mongo.db.conductores.find_one({'cedula': cedula})
        return existing_conductor is not None

    def edit_conductor_by_id(self, conductor_id, nuevo_nombres, nueva_cedula, nuevo_telefono, nueva_fecha_nacimiento, nuevo_correo, nuevo_genero_id, nuevo_trailer_id):
        self.mongo.db.conductores.update_one(
            {'_id': ObjectId(conductor_id)},
            {'$set': {
                'nombre': nuevo_nombres,
                'cedula': nueva_cedula,
                'telefono': nuevo_telefono,
                'fecha_nacimiento': nueva_fecha_nacimiento,
                'correo': nuevo_correo,
                'genero_id': nuevo_genero_id,
                'trailer_id': ObjectId(nuevo_trailer_id),
                'eliminado': False  # Establecer eliminado en False al editar
            }}
        )
        
    def delete_conductor(self, conductor_id):
        conductor = self.mongo.db.conductores.find_one(
            {'_id': ObjectId(conductor_id)})

        if conductor:
            genero = self.mongo.db.generos.find_one(
                {'_id': conductor['genero_id']})
            trailer = self.mongo.db.trailer.find_one(
                {'_id': conductor['trailer_id']})
        else:
            genero = None
            trailer = None

        if conductor:
            # Actualizar eliminado a True en lugar de eliminar físicamente
            self.mongo.db.conductores.update_one({'_id': ObjectId(conductor_id)},
                                                 {'$set': {'eliminado': True}})
        return conductor, genero, trailer
    
#########################################################################################################################
     # RUTAS
    
    def get_rutas(self):
        rutas = self.mongo.db.rutas.find()
        clientes = {str(cliente['_id']): cliente['nombres']
                    for cliente in self.mongo.db.clientes.find()}
        conductores = {str(conductor['_id']): conductor['nombre']
                    for conductor in self.mongo.db.conductores.find()}
        provincias = {str(provincia['_id']): provincia['nombre']
                    for provincia in self.mongo.db.provincias.find()}
        tipos_carga = {str(tipo['_id']): tipo['nombre']
                    for tipo in self.mongo.db.tipo_carga.find()}
        categorias_carga = {str(categoria['_id']): categoria['nombre']
                            for categoria in self.mongo.db.categoria_carga.find()}

        rutas_con_info = []

        for ruta in rutas:
            cliente_id = str(ruta.get('cliente'))
            cliente_nombre = clientes.get(cliente_id, 'Cliente Desconocido')

            conductor_id = str(ruta.get('conductor_responsable'))
            conductor_nombre = conductores.get(conductor_id, 'Conductor Desconocido')

            provincia_inicio_id = str(ruta.get('provincia_inicio'))
            provincia_inicio_nombre = provincias.get(provincia_inicio_id, 'Provincia Desconocida')

            provincia_fin_id = str(ruta.get('provincia_fin'))
            provincia_fin_nombre = provincias.get(provincia_fin_id, 'Provincia Desconocida')

            tipo_carga_id = str(ruta.get('tipos_carga'))
            tipo_carga_nombre = tipos_carga.get(tipo_carga_id, 'Tipo de Carga Desconocido')

            categoria_carga_id = str(ruta.get('categoria_carga'))
            categoria_carga_nombre = categorias_carga.get(categoria_carga_id, 'Categoría de Carga Desconocida')

            ubicacion_inicio = ruta.get('ubicacion_inicio', 'Ubicación Desconocida')
            ubicacion_fin = ruta.get('ubicacion_fin', 'Ubicación Desconocida')


            ruta_con_info = {
                '_id': str(ruta['_id']),
                'cliente': cliente_nombre,
                'conductor_responsable': conductor_nombre,
                'provincia_inicio': provincia_inicio_nombre,
                'hora_inicio': ruta.get('hora_inicio', 'Hora Desconocida'),
                'ubicacion_inicio': ubicacion_inicio,
                'provincia_fin': provincia_fin_nombre,
                'hora_fin': ruta.get('hora_final', 'Hora Desconocida'),
                'ubicacion_fin': ubicacion_fin,
                'tipo_carga': tipo_carga_nombre,
                'categoria_carga': categoria_carga_nombre
            }

            rutas_con_info.append(ruta_con_info)

        return rutas_con_info



    def add_ruta(self, cliente_id, conductor_id, provincia_inicio_id, hora_inicio, ubicacion_inicio, provincia_fin_id, hora_fin, ubicacion_fin, tipo_carga_id, categoria_carga_id):
        nueva_ruta = {
            'cliente': ObjectId(cliente_id),
            'conductor_responsable': ObjectId(conductor_id),
            'provincia_inicio': (provincia_inicio_id),
            'hora_inicio': datetime.strptime(hora_fin, '%Y-%m-%dT%H:%M'),
            'ubicacion_inicio': ubicacion_inicio,
            'provincia_fin': (provincia_fin_id),
            'hora_final': datetime.strptime(hora_fin, '%Y-%m-%dT%H:%M'),
            'ubicacion_fin': ubicacion_fin,
            'tipos_carga': (tipo_carga_id),
            'categoria_carga': (categoria_carga_id)
        }
        self.mongo.db.rutas.insert_one(nueva_ruta)

    # Añade esta función en tu clase que maneja las rutas
    def guardar_ruta_editada(self, ruta_id, valores_anteriores, valores_nuevos):
        ruta_editada_data = {
            'ruta_id': ruta_id,
            'valores_anteriores': valores_anteriores,
            'valores_nuevos': valores_nuevos,
            'fecha_edicion': datetime.utcnow()
        }
        self.mongo.db.rutas_edited.insert_one(ruta_editada_data)

    # Modifica tu función edit_ruta_by_id para incluir el trigger
    def edit_ruta_by_id(self, ruta_id, cliente_id, conductor_id, provincia_inicio_id, hora_inicio, ubicacion_inicio, provincia_fin_id, hora_fin, ubicacion_fin, tipo_carga_id, categoria_carga_id):
        # Obtener valores anteriores antes de realizar la actualización
        ruta_anterior = self.mongo.db.rutas.find_one({'_id': ObjectId(ruta_id)})

        valores_anteriores = {
            'cliente': str(ruta_anterior.get('cliente')),
            'conductor_responsable': str(ruta_anterior.get('conductor_responsable')),
            'provincia_inicio': str(ruta_anterior.get('provincia_inicio')),
            'hora_inicio': str(ruta_anterior.get('hora_inicio')),
            'ubicacion_inicio': str(ruta_anterior.get('ubicacion_inicio')),
            'provincia_fin': str(ruta_anterior.get('provincia_fin')),
            'hora_final': str(ruta_anterior.get('hora_final')),
            'ubicacion_fin': str(ruta_anterior.get('ubicacion_fin')),
            'tipos_carga': str(ruta_anterior.get('tipos_carga')),
            'categoria_carga': str(ruta_anterior.get('categoria_carga'))
        }

        # Realizar la actualización
        self.mongo.db.rutas.update_one(
            {'_id': ObjectId(ruta_id)},
            {'$set': {
                'cliente': ObjectId(cliente_id),
                'conductor_responsable': ObjectId(conductor_id),
                'provincia_inicio': provincia_inicio_id,
                'hora_inicio': datetime.strptime(hora_inicio, '%Y-%m-%dT%H:%M'),
                'ubicacion_inicio': ubicacion_inicio,
                'provincia_fin': provincia_fin_id,
                'hora_final': datetime.strptime(hora_fin, '%Y-%m-%dT%H:%M'),
                'ubicacion_fin': ubicacion_fin,
                'tipos_carga': tipo_carga_id,
                'categoria_carga': categoria_carga_id
            }}
        )

        # Obtener los nuevos valores después de la actualización
        ruta_nueva = self.mongo.db.rutas.find_one({'_id': ObjectId(ruta_id)})

        valores_nuevos = {
            'cliente': str(ruta_nueva.get('cliente')),
            'conductor_responsable': str(ruta_nueva.get('conductor_responsable')),
            'provincia_inicio': str(ruta_nueva.get('provincia_inicio')),
            'hora_inicio': str(ruta_nueva.get('hora_inicio')),
            'ubicacion_inicio': str(ruta_nueva.get('ubicacion_inicio')),
            'provincia_fin': str(ruta_nueva.get('provincia_fin')),
            'hora_final': str(ruta_nueva.get('hora_final')),
            'ubicacion_fin': str(ruta_nueva.get('ubicacion_fin')),
            'tipos_carga': str(ruta_nueva.get('tipos_carga')),
            'categoria_carga': str(ruta_nueva.get('categoria_carga'))
        }

        # Llamar a la función para guardar la edición
        self.guardar_ruta_editada(ruta_id, valores_anteriores, valores_nuevos)


    def delete_ruta(self, ruta_id):
        ruta = self.mongo.db.rutas.find_one({'_id': ObjectId(ruta_id)})

        if ruta:
            cliente = self.mongo.db.clientes.find_one({'_id': ruta['cliente']})
            conductor = self.mongo.db.conductores.find_one({'_id': ruta['conductor_responsable']})
        else:
            cliente = None
            conductor = None

        if ruta:
            # Almacenar la fecha de eliminación y los datos de la ruta eliminada
            deleted_ruta_data = {
                'ruta_id': ruta['_id'],
                'cliente_id': str(cliente['_id']) if cliente else 'Desconocido',
                'conductor_id': str(conductor['_id']) if conductor else 'Desconocido',
                'provincia_inicio': ruta['provincia_inicio'],
                'hora_inicio': ruta['hora_inicio'],
                'ubicacion_inicio': ruta['ubicacion_inicio'],
                'provincia_fin': ruta['provincia_fin'],
                'hora_final': ruta['hora_final'],
                'ubicacion_fin': ruta['ubicacion_fin'],
                'tipos_carga': ruta['tipos_carga'],
                'categoria_carga': ruta['categoria_carga'],
                'fecha_eliminacion': datetime.utcnow()
            }

            # Insertar los datos de la ruta eliminada en la colección rutas_deleted
            self.mongo.db.rutas_deleted.insert_one(deleted_ruta_data)

            # Eliminar la ruta de la colección principal
            self.mongo.db.rutas.delete_one({'_id': ObjectId(ruta_id)})

        return ruta, cliente, conductor