create database tienda_libros;
use tienda_libros;

DROP TABLE libros;
create table libros(
	id int primary key auto_increment,
    autor varchar(60) not null,
    titulo varchar(60) not null,
    fecha_publicacion datetime,
    edicion_id int
);

create table editores(
    editor_id int primary key auto_increment,
    nombre varchar(60) not null,
    correo varchar(60),
    domicilio varchar(100),
    telefono varchar(30),
    notas varchar(1000)
);

drop table ediciones;
create table ediciones(
	edicion_id int primary key auto_increment,
    editor_id int not null,
    numero_edicion int not null,
    nombre_edicion varchar(255),
    fecha_edicion datetime,
	stock int,
    isbn varchar(40),
    url_imagen_tapa varchar(100),
    url_imagen_trasera varchar(100),
    paginas int,
    tamanio varchar(20)
);
select * from ediciones;
select * from libros;

-- drop table libros;
/* comento que este es un código viejo
create table libros(
	id int primary key auto_increment,
    autor varchar(60),
    titulo varchar(60),
    fecha_publicacion datetime,
    paginas int,
    editor_id int,
    tamanio varchar(13)
);
*/
select * from ediciones;
