var coloresBlancos = db.trailer.trailer.find({ "color": 1 }).map(function(trailer) {
    return db.tuColeccion.colores.findOne({ "_id": trailer.color }).nombre;
});

printjson(coloresBlancos);
