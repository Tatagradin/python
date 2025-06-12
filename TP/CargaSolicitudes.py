
from Conexiones import Conexion
from Clases import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte

import csv

class CargadorDeDatos:
    def __init__(self, red_transporte):
        """
        Constructor que recibe una instancia de la clase RedTransporte para agregar las ciudades y conexiones.
        """
        self.red_transporte = red_transporte

    def cargar_solicitudes(self, archivo_solicitudes):
        """Carga las solicitudes desde un archivo CSV y las agrega a la red de transporte."""
        with open(archivo_solicitudes, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la primera fila (cabecera del archivo)
            for row in reader:
                if len(row) < 4:  # Verificar que la fila tiene al menos 4 elementos
                    print(f"Fila ignorada debido a formato incorrecto: {row}")
                    continue  # Si la fila no tiene 4 columnas, se ignora

                id_solicitud = row[0]  # `id_carga`
                peso = int(row[1])  # `peso_kg`
                origen = row[2]  # `origen`
                destino = row[3]  # `destino`

                # Obtener las ciudades de la red de transporte
                ciudad_origen = self.red_transporte.get_ciudad(origen)
                ciudad_destino = self.red_transporte.get_ciudad(destino)

                if ciudad_origen and ciudad_destino:
                    # Crear la solicitud con los datos
                    solicitud = solicitud(id_solicitud, peso, ciudad_origen, ciudad_destino)
                    self.red_transporte.agregar_solicitud(solicitud)  # Agregar la solicitud a la red

# Uso de la clase CargadorDeDatos
# Suponiendo que tienes la clase RedTransporte ya definida

# 1. Crear la instancia de RedTransporte
red_transporte = RedTransporte()

# 2. Crear el cargador de datos
cargador = CargadorDeDatos(red_transporte)

# 3. Cargar las solicitudes desde el archivo CSV
cargador.cargar_solicitudes('TP/solicitudes.csv')  # Ajusta la ruta del archivo según sea necesario
