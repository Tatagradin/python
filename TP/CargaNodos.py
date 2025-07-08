from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte
from CargadorGRAL import Cargador

import csv

class CargadorDeNodos(Cargador):
    def __init__(self, red_transporte):
        self.red_transporte = red_transporte

    def cargar_nodos(self, archivo_nodos):
        """Carga los nodos (ciudades) desde un archivo CSV y los agrega a la red de transporte."""
        try:
            # Usar función común para leer el archivo
            filas = CargadorDeNodos.leer_csv_comun(archivo_nodos)
            
            ciudades_cargadas = 0
            for row in filas:
                if len(row) < 1:  # Verificar que la fila tiene al menos 1 elemento
                    print(f"Fila ignorada debido a formato incorrecto: {row}")
                    continue

                ciudad_nombre = row[0].strip()  # strip Elimina espacios en blanco
                
                # Verificar si la ciudad ya existe
                if self.red_transporte.get_ciudad(ciudad_nombre):
                    print(f"Advertencia: La ciudad '{ciudad_nombre}' ya existe. Ignorando duplicado.")
                    continue
                
                # Crear la ciudad y agregarla a la red
                ciudad = Ciudad(ciudad_nombre)
                self.red_transporte.agregar_ciudad(ciudad)
                ciudades_cargadas += 1
            
        except Exception as e:
            raise Exception(f"Error al cargar nodos: {str(e)}")
    
