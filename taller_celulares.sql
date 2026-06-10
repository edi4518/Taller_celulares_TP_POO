CREATE DATABASE taller_celulares;

CREATE TABLE clientes (
id_cliente INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(25) NOT NULL,
apellido VARCHAR(25) NOT NULL,
documento VARCHAR(20) NOT NULL,
telefono VARCHAR(12) NOT NULL,
correo VARCHAR(35) NOT NULL
)

CREATE TABLE tecnicos(
id_tecnico INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(25) NOT NULL,
apellido VARCHAR(25) NOT NULL,
documento VARCHAR(15) NOT NULL,
telefono VARCHAR(12) NOT NULL,
turno VARCHAR(20) NOT NULL
)



CREATE TABLE dispositivos (
imei VARCHAR(15) PRIMARY KEY,
marca VARCHAR(25) NOT NULL,
modelo VARCHAR(25) NOT NULL,
cliente_id INT NOT NULL,

FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente)
	ON DELETE restrict
	ON UPDATE CASCADE
)

CREATE TABLE reparaciones(
id_reparacion INT AUTO_INCREMENT PRIMARY KEY,
falla VARCHAR(60) NOT NULL,
fecha_ingreso DATETIME DEFAULT CURRENT_TIMESTAMP,
estado VARCHAR(30) NOT NULL DEFAULT 'INGRESADO',
notas TEXT NULL,

dispositivo_imei VARCHAR(15) NOT NULL,
tecnico_id INT NOT NULL,

#Establecemos las relaciones 

FOREIGN KEY (dispositivo_imei) REFERENCES dispositivos(imei)
	ON DELETE restrict
	ON UPDATE CASCADE,
	
FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id_tecnico)
	ON DELETE restrict
	ON UPDATE CASCADE
)

SELECT * FROM dispositivos;

SELECT * FROM reparaciones;

SELECT * FROM clientes;
SELECT * FROM tecnicos;



SELECT r.id_reparacion, r.falla, r.estado, r.fecha_ingreso, r.notas, d.imei, d.marca, d.modelo, c.documento, c.telefono, c.correo, c.nombre AS nombre_cliente, c.apellido AS apellido_cliente FROM reparaciones r INNER JOIN dispositivos d ON r.dispositivo_imei = d.imei INNER JOIN clientes c ON d.cliente_id = c.id_cliente