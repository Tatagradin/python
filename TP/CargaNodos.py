from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte

import csv

class CargadorDeNodos:
    def __init__(self, red_transporte):

        self.red_transporte = red_transporte

    def cargar_nodos(self, archivo_nodos):

        try:
            with open(archivo_nodos, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la primera fila (cabecera del archivo)
                
                ciudades_cargadas = 0
                for row in reader:
                    if len(row) < 1:  # Verificar que la fila tiene al menos 1 elemento
                        print(f"Fila ignorada debido a formato incorrecto: {row}")
                        continue

                    ciudad_nombre = row[0].strip()  # Eliminar espacios en blanco
                    if not ciudad_nombre:  # Verificar que el nombre no esté vacío
                        print(f"Fila ignorada: nombre de ciudad vacío")
                        continue
                    
                    # Verificar si la ciudad ya existe
                    if self.red_transporte.get_ciudad(ciudad_nombre):
                        print(f"Advertencia: La ciudad '{ciudad_nombre}' ya existe. Ignorando duplicado.")
                        continue
                    
                    # Crear la ciudad y agregarla a la red
                    ciudad = Ciudad(ciudad_nombre)
                    self.red_transporte.agregar_ciudad(ciudad)
                    ciudades_cargadas += 1
                
                if ciudades_cargadas == 0:
                    raise Exception("No se pudo cargar ninguna ciudad. Verifique el archivo nodos.csv")
                    
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo {archivo_nodos}")
        except Exception as e:
            raise Exception(f"Error al cargar nodos: {str(e)}")
    
