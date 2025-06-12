
from Conexiones import Conexion
from Clases import Ciudad
from Vehiculos import *


class RedTransporte:
    def __init__(self):
        self.ciudades = {}        # Diccionario para almacenar las ciudades por nombre
        self.conexiones = []      # Lista global que guarda todas las conexiones

    def agregar_ciudad(self, ciudad):
        """ Agrega una ciudad al diccionario de ciudades usando el nombre como clave """
        self.ciudades[ciudad.nombre] = ciudad

    def agregar_conexion(self, conexion):
        """ Agrega una conexión a la red de transporte y la registra en ambas ciudades involucradas """
        # Primero se agrega la conexión a la lista global de la red
        self.conexiones.append(conexion)

        # Luego, se agrega la conexión a las listas locales de las dos ciudades involucradas
        conexion.ciudad1.agregar_conexion(conexion)  # Registra en la ciudad1
        conexion.ciudad2.agregar_conexion(conexion)  # Registra en la ciudad2

    def get_ciudad(self, nombre):
        """ Devuelve el objeto Ciudad por su nombre """
        return self.ciudades.get(nombre)

    def get_conexiones_desde(self, nombre_ciudad):
        """ Devuelve todas las conexiones salientes desde una ciudad """
        ciudad = self.get_ciudad(nombre_ciudad)
        if ciudad:
            return ciudad.posibles_conexiones
        return []

    def filtrar_conexiones_validas(self, vehiculo):
        """ Filtra las conexiones válidas según el tipo de vehículo y las restricciones """
        conexiones_validas = []
        for conexion in self.conexiones:
            # Verificamos si el modo de transporte de la conexión es compatible con el vehículo
            if conexion.tipo_transporte != vehiculo.__class__.__name__.lower():
                continue  # Ejemplo: "aereo" vs "ferroviario"

            # Validamos las restricciones de tipo de transporte o condiciones especiales
            if conexion.tipo_restriccion == "tipo":
                tipo_conexion = conexion.restriccion
                if isinstance(vehiculo, Maritimo) and tipo_conexion not in ["maritimo", "fluvial"]:
                    continue

            if conexion.tipo_restriccion == "prob_mal_tiempo" and isinstance(vehiculo, Aereo):
                if float(conexion.restriccion) > 0:
                    vehiculo.velocidad = 400  # Ajustamos la velocidad si hay mal tiempo

            conexiones_validas.append(conexion)
        return conexiones_validas