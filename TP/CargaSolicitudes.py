from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte
from Solicitud import Solicitud
from leector_csv import leer_csv_comun

import csv

class CargadorDeDatos:
    def __init__(self, red_transporte):
        self.red_transporte = red_transporte

    def cargar_solicitudes(self, archivo_solicitudes):
        """Carga las solicitudes desde un archivo CSV y las agrega a la red de transporte."""
        try:
            # Usar función común para leer el archivo
            filas = leer_csv_comun(archivo_solicitudes)
            
            for row in filas:
                if len(row) < 4:  # Verificar que la fila tiene al menos 4 elementos
                    print(f"Fila ignorada debido a formato incorrecto: {row}")
                    continue
                
                id_solicitud = row[0].strip()
                peso = row[1].strip()  
                origen = row[2].strip()
                destino = row[3].strip()

                ciudad_origen = self.red_transporte.get_ciudad(origen)
                ciudad_destino = self.red_transporte.get_ciudad(destino)

                if not ciudad_origen:
                    print(f"Nota: Ciudad de origen '{origen}' no encontrada en la primera pasada. Se intentará cargar nuevamente.")
                    continue
                if not ciudad_destino:
                    print(f"Nota: Ciudad de destino '{destino}' no encontrada en la primera pasada. Se intentará cargar nuevamente.")
                    continue

                try:
                    solicitud = Solicitud(id_solicitud, peso, ciudad_origen, ciudad_destino)
                    self.red_transporte.agregar_solicitud(solicitud)
                    print(f"Solicitud cargada: {solicitud}")
                except ValueError as e:
                    print(f"Error al cargar solicitud '{id_solicitud}': {e}")

        except Exception as e:
            raise Exception(f"Error al cargar solicitudes: {str(e)}")