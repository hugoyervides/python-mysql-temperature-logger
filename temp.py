#!/usr/bin/python
# Importar todo lo necesario
import os
import sys
import time
import MySQLdb
#Define los parametros MySQL AQUI!
ip = "192.168.15.202"
usuario = "victor"
password = "password"
database = "IOT"
#La base de datos guarda desde donde se estan capturando los datos, introduce un nombre que identifique el lugar donde se recolectan los datos
ubicacion = "DEPA_HUGO"
#Despelgar mensaje al usuario
print("Estableciendo Conexion cons servidor MySQL ...")
print("Conectando con " + ip )
#Establecer conexion MySQL
db = MySQLdb.connect(host= ip, user= usuario , passwd= password , db= database)
#Arrancar cursor
cur = db.cursor()
#Arrancar los valores viejos para que entren en la condicion cuando se arranca el script
oldtemp = 0
oldhum = 0

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #Revisar si los datos son nuevos o si son ya actuales para no molestar a la base de datos
    if temperature != oldtemp:
        #Subir temperatura a servidor MySQL
        cur.execute("UPDATE mont SET temp = (%s) WHERE loc = (%s)" , (temperature, ubicacion))
        db.commit()
        #Indicar el cambio de temperatura
        print("Cambio de temperatura detectado, Actualizando tabla MySQL .. Nueva Temperatura: " + temperature + " C")
        #Actualizar el valor de temperatura vieja
        oldtemp = temperature
    if humidity != oldhum:
        #Subir humedad a servidor MySQL
        cur.execute("UPDATE mont SET hum = (%s) WHERE id = (%s)" , (humidity, ubicacion))
        db.commit()
        #Indicar el cambio de humedad
        print("Cambio de humedad detectado, Actualizando tabla MySQL .. Nueva Humedad: " + humidity + " %")
        oldhum = humidity
    #Poner timer para evitar flood a servidor MySQL
    time.sleep(5)

#Cerrar las conexiones