#!/bin/bash

# Este script se encarga de
# 1. Instalar MySQL
# 2. Crear una base de datos "alimentador"
# 3. Crear una tabla en la bdd
# 4. Popular la tabla con datos dummie

# Verificar si MySQL está instalado
if ! command -v mysql &> /dev/null
then
    echo "**MySQL no está instalado. Instalando ahora...**"
    sudo apt update
    sudo apt install mysql-server
else
    echo "**MySQL ya está instalado.**"
fi

# Crear la base de datos y la tabla
echo "**Creando la base de datos y la tabla...**"
sudo mysql -u root -p<<MYSQL_SCRIPT
CREATE DATABASE IF NOT EXISTS alimentador;
USE alimentador;

CREATE TABLE IF NOT EXISTS datos (
    porcentaje_contenedor VARCHAR(5),
    fecha VARCHAR(29),
    morning VARCHAR(20),
    morning_porcion VARCHAR(5),
    lunch VARCHAR(20),
    lunch_porcion VARCHAR(5),
    dinner VARCHAR(20),
    dinner_porcion VARCHAR(5),
    porcion VARCHAR(5),
    ultima_comida VARCHAR(29)
);
MYSQL_SCRIPT

# Llenar la tabla con datos ficticios
echo "**Llenando la tabla con datos ficticios...**"
for i in {1..100}
do
    porcentaje=$((RANDOM%101))
    porcion=$((RANDOM%101))
    fecha=$(date +"%d/%m/%Y:%H:%M:%S" -d "$i days")
    morning=$(date +"%d/%m/%Y:%H:%M:%S" -d "$((i-1)) days")
    morning_porcion=$((RANDOM%101))
    lunch=$(date +"%d/%m/%Y:%H:%M:%S" -d "$((i-1)) days")
    lunch_porcion=$((RANDOM%101))
    dinner=$(date +"%d/%m/%Y:%H:%M:%S" -d "$((i-1)) days")
    dinner_porcion=$((RANDOM%101))
    ultima_comida=$(date +"%d/%m/%Y:%H:%M:%S" -d "$((i-1)) days")

    sudo mysql -u root -p<<MYSQL_SCRIPT
    USE alimentador;
    INSERT INTO datos (porcentaje_contenedor, fecha, morning, morning_porcion, lunch, lunch_porcion, dinner, dinner_porcion, porcion, ultima_comida) VALUES ("$porcentaje", "$fecha", "$morning", "$morning_porcion", "$lunch", "$lunch_porcion", "$dinner", "$dinner_porcion", "$porcion", "$ultima_comida");
MYSQL_SCRIPT
done

echo "**¡Todo listo! Ahora puedes conectarte a la base de datos 'alimentador'.**"