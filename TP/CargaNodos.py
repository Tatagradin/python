from Conexiones import Conexion
from Clases import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte

import csv

class CargadorDeNodos:
    def __init__(self, red_transporte):
        """
        Constructor que recibe una instancia de la clase RedTransporte para agregar las ciudades.
        """
        self.red_transporte = red_transporte

    def cargar_nodos(self, archivo_nodos):
        """Carga los nodos (ciudades) desde un archivo CSV y los agrega a la red de transporte."""
        with open(archivo_nodos, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la primera fila (cabecera del archivo)
            for row in reader:
                if len(row) < 1:  # Verificar que la fila tiene al menos 1 elemento
                    print(f"Fila ignorada debido a formato incorrecto: {row}")
                    continue  # Si la fila no tiene suficientes columnas, se ignora

                ciudad_nombre = row[0]  # `ciudad`
                
                # Crear la ciudad y agregarla a la red
                ciudad = Ciudad(ciudad_nombre)
                self.red_transporte.agregar_ciudad(ciudad)  # Agregar la ciudad a la red

# Uso de la clase CargadorDeNodos
# Suponiendo que tienes la clase RedTransporte ya definida

# 1. Crear la instancia de RedTransporte
red_transporte = RedTransporte()

# 2. Crear el cargador de datos para nodos
cargador_nodos = CargadorDeNodos(red_transporte)

# 3. Cargar los nodos desde el archivo CSV
cargador_nodos.cargar_nodos('TP/nodos.csv')  # Ajusta la
