from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte
from Solicitud import Solicitud

import csv

class CargadorDeDatos:
    def __init__(self, red_transporte):
        """
        Constructor que recibe una instancia de la clase RedTransporte para agregar las solicitudes.
        """
        self.red_transporte = red_transporte

    def cargar_solicitudes(self, archivo_solicitudes):
        """Carga las solicitudes desde un archivo CSV y las agrega a la red de transporte."""
        try:
            with open(archivo_solicitudes, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la primera fila (cabecera del archivo)
                for row in reader:
                    if len(row) < 4:  # Verificar que la fila tiene al menos 4 elementos
                        print(f"Fila ignorada debido a formato incorrecto: {row}")
                        continue

                    id_solicitud = row[0]  # `id_carga`
                    try:
                        peso = int(row[1])  # `peso_kg`
                    except ValueError:
                        print(f"Error: El peso debe ser un número entero. Fila ignorada: {row}")
                        continue

                    origen = row[2]  # `origen`
                    destino = row[3]  # `destino`

                    # Obtener las ciudades de la red de transporte
                    ciudad_origen = self.red_transporte.get_ciudad(origen)
                    ciudad_destino = self.red_transporte.get_ciudad(destino)

                    if not ciudad_origen:
                        print(f"Error: Ciudad de origen '{origen}' no encontrada. Fila ignorada: {row}")
                        continue
                    if not ciudad_destino:
                        print(f"Error: Ciudad de destino '{destino}' no encontrada. Fila ignorada: {row}")
                        continue

                    # Crear la solicitud con los datos
                    solicitud = Solicitud(id_solicitud, peso, ciudad_origen, ciudad_destino)
                    self.red_transporte.agregar_solicitud(solicitud)
                    print(f"Solicitud cargada: {solicitud}")

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {archivo_solicitudes}")
        except Exception as e:
            print(f"Error al cargar solicitudes: {str(e)}")

# Uso de la clase CargadorDeDatos
# Suponiendo que tienes la clase RedTransporte ya definida

# 1. Crear la instancia de RedTransporte
red_transporte = RedTransporte()

# 2. Crear el cargador de datos
cargador = CargadorDeDatos(red_transporte)

# 3. Cargar las solicitudes desde el archivo CSV
cargador.cargar_solicitudes('TP/solicitudes.csv')  # Ajusta la ruta del archivo según sea necesario
