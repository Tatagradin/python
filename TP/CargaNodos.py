from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte
from CargadorGRAL import Cargador

import csv

class CargadorDeNodos(Cargador):
    def __init__(self, red_transporte):
        super().__init__(red_transporte)

    def cargar_nodos(self, archivo_nodos):
        """Carga los nodos (ciudades) desde un archivo CSV y los agrega a la red de transporte."""
        try:
       
            filas = CargadorDeNodos.leer_csv_comun(archivo_nodos)
            
            ciudades_cargadas = 0
            for row in filas:
                if len(row) < 1:  
                    print(f"Fila ignorada debido a formato incorrecto: {row}")
                    continue

                ciudad_nombre = row[0].strip() 
                
             
                if self.red_transporte.get_ciudad(ciudad_nombre):
                    print(f"Advertencia: La ciudad '{ciudad_nombre}' ya existe. Ignorando duplicado.")
                    continue
                
                # Crear la ciudad y agregarla a la red
                ciudad = Ciudad(ciudad_nombre)
                self.red_transporte.agregar_ciudad(ciudad)
                ciudades_cargadas += 1
            
        except Exception as e:
            raise Exception(f"Error al cargar nodos: {str(e)}")
    
