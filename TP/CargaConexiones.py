from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte

import csv

class CargadorDeConexiones:
    def __init__(self, red_transporte):
        """
        Constructor que recibe una instancia de la clase RedTransporte para agregar las conexiones.
        """
        self.red_transporte = red_transporte

    def cargar_conexiones(self, archivo_conexiones):
        """Carga las conexiones desde un archivo CSV y las agrega a la red de transporte."""
        with open(archivo_conexiones, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la primera fila (cabecera del archivo)
            for row in reader:
                if len(row) < 5:  # Verificar que la fila tiene al menos 5 elementos
                    print(f"Fila ignorada debido a formato incorrecto: {row}")
                    continue  # Si la fila no tiene suficientes columnas, se ignora

                ciudad1_nombre = row[0]  # `origen`
                ciudad2_nombre = row[1]  # `destino`
                tipo_transporte = row[2]  # `tipo`
                try:
                    distancia = int(row[3])  # `distancia_km`
                except ValueError:
                    print(f"Error en la fila {row}: La distancia debe ser un número, pero se encontró '{row[3]}'")
                    continue  # Si hay error en la distancia, saltamos esta fila
                tipo_restriccion = row[4] if row[4] else None  # `restriccion`
                restriccion = row[5] if row[5] else None  # `valor_restriccion`

                # Obtener las ciudades de la red de transporte
                ciudad1 = self.red_transporte.get_ciudad(ciudad1_nombre)
                ciudad2 = self.red_transporte.get_ciudad(ciudad2_nombre)

                if ciudad1 and ciudad2:
                    # Crear la conexión con los datos
                    conexion = Conexion(ciudad1, ciudad2, distancia, tipo_transporte, tipo_restriccion, restriccion)
                    self.red_transporte.agregar_conexion(conexion)  # Agregar la conexión a la red

# Uso de la clase CargadorDeConexiones
# Suponiendo que tienes la clase RedTransporte ya definida

# 1. Crear la instancia de RedTransporte
red_transporte = RedTransporte()

# 2. Crear el cargador de datos para conexiones
cargador_conexiones = CargadorDeConexiones(red_transporte)

# 3. Cargar las conexiones desde el archivo CSV
cargador_conexiones.cargar_conexiones('TP/conexiones.csv')  # Ajusta la ruta del archivo según sea necesario
