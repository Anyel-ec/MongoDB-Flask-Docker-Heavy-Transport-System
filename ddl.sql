create table rutas(
id_rutas int serial primary key, 
cliente varchar(50),
provincia_inicial varchar(50),
provincia_final varchar(50),
fecha_inicial datetime,
fecha_final datetime,
ubicacion_inicio varchar(50), 
ubicacion_final varchar(50), 
tipo_carga varchar(50), 
categoria_carga varchar(50), 
conductor varchar(50), 
placa varchar(8)
);

create table estado_vias(
id_estados int serial primary key, 
provincia varchar(50), 
tipo varchar(50), 
tramo varchar(100), 
estado varchar(50), 
obras_pendientes boolean
);

create table mantenimiento(
id_mantenimiento int serial primary key, 
inicio_mantenimiento date, 
tipo_mantenimiento varchar(50), 
ubicacion_mantenimiento varchar(50),
fin_mantenimiento date, 

);