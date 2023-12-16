# routes/trailer.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
# Configuración de la base de datos MongoDB desde la variable de entorno
app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
trailer_bp = Blueprint('trailer', __name__)
mongo = PyMongo()


@trailer_bp.route('/')
def index():
    trailers = mongo.db.trailer.find()
    colores = {color['_id']: color['nombre'] for color in mongo.db.colores.find()}
    marcas = {marca['_id']: marca['nombre'] for marca in mongo.db.marcas.find()}
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

    return render_template('index.html', trailers=trailers_con_colores)

@trailer_bp.route('/agregar_trailer', methods=['POST'])
def agregar_trailer():
    if request.method == 'POST':
        # Obtener los datos del formulario
        matricula = request.form.get('matricula')
        Ejes = int(request.form.get('Ejes'))
        marca_id = int(request.form.get('marca'))
        modelo = request.form.get('modelo')
        color_id = int(request.form.get('color'))
        capacidad_carga = int(request.form.get('capacidadCarga'))

        nuevo_trailer = {
            'matricula': matricula,
            'Ejes': Ejes,
            'marca_id': marca_id,
            'modelo': modelo,
            'color_id': color_id,
            'capacidad_carga': capacidad_carga
        }

        mongo.db.trailer.insert_one(nuevo_trailer)
        flash('Trailer agregado correctamente', 'success')
        return redirect(url_for('trailer.index'))

@trailer_bp.route('/editar_trailer/<string:matricula>', methods=['GET', 'POST'])
def editar_trailer(matricula):
    trailer = mongo.db.trailer.find_one({'matricula': matricula})

    if request.method == 'POST':
        nuevo_modelo = request.form.get('modelo')
        nuevo_color_id = int(request.form.get('color'))
        nueva_capacidad_carga = int(request.form.get('capacidadCarga'))

        mongo.db.trailer.update_one(
            {'matricula': matricula},
            {'$set': {
                'modelo': nuevo_modelo,
                'color_id': nuevo_color_id,
                'capacidad_carga': nueva_capacidad_carga
            }}
        )

        flash('Trailer actualizado correctamente', 'success')
        return redirect(url_for('trailer.index'))

    colores = mongo.db.colores.find()
    marcas = mongo.db.marcas.find()

    return render_template('actualizarTrailer.html', trailer=trailer, colores=colores, marcas=marcas)

@trailer_bp.route('/eliminar_trailer/<string:matricula>', methods=['GET', 'POST'])
def eliminar_trailer(matricula):
    trailer = mongo.db.trailer.find_one({'matricula': matricula})

    if trailer:
        marca = mongo.db.marcas.find_one({'_id': trailer['marca_id']})
        color = mongo.db.colores.find_one({'_id': trailer['color_id']})
    else:
        marca = None
        color = None

    if request.method == 'POST':
        mongo.db.trailer.delete_one({'matricula': matricula})
        flash('Trailer eliminado correctamente', 'success')
        return redirect(url_for('trailer.index'))

    return render_template('eliminarTrailer.html', trailer=trailer, marca=marca, color=color)
