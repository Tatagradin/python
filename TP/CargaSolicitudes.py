from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte
from Solicitud import Solicitud

import csv

class CargadorDeDatos:
    def __init__(self, red_transporte):
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

                    origen = row[2].strip()  # `origen` - eliminar espacios en blanco
                    destino = row[3].strip()  # `destino` - eliminar espacios en blanco

                    # Obtener las ciudades de la red de transporte
                    ciudad_origen = self.red_transporte.get_ciudad(origen)
                    ciudad_destino = self.red_transporte.get_ciudad(destino)

                    if not ciudad_origen:
                        print(f"Nota: Ciudad de origen '{origen}' no encontrada en la primera pasada. Se intentará cargar nuevamente.")
                        continue
                    if not ciudad_destino:
                        print(f"Nota: Ciudad de destino '{destino}' no encontrada en la primera pasada. Se intentará cargar nuevamente.")
                        continue

                    # Crear la solicitud con los datos
                    solicitud = Solicitud(id_solicitud, peso, ciudad_origen, ciudad_destino)
                    self.red_transporte.agregar_solicitud(solicitud)
                    print(f"Solicitud cargada: {solicitud}")

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {archivo_solicitudes}")
        except Exception as e:
            print(f"Error al cargar solicitudes: {str(e)}")