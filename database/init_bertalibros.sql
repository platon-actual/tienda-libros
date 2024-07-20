create database tienda_libros;
use tienda_libros;

create table libros(
	id int primary key auto_increment,
    autor varchar(60),
    titulo varchar(60),
    fecha_publicacion datetime,
    paginas int,
    editor_id int,
    tamanio varchar(13)
);

create table editores(
    editor_id int primary key auto_increment,
    nombre varchar(60) not null,
    correo varchar(60),
    domicilio varchar(100),
    notas varchar(1000)
);

create table ediciones(
	edicion_id int primary key auto_increment,
    editor_id int not null,
    numero_edicion int not null,
    fecha_edicion datetime,
	stock int,
    isbn varchar(30),
    imagen varchar(100)
);

select * from libros;