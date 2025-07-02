from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte

import csv

class CargadorDeConexiones:
    def __init__(self, red_transporte):

        self.red_transporte = red_transporte

    def cargar_conexiones(self, archivo_conexiones):

        try:
            with open(archivo_conexiones, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la primera fila (cabecera del archivo)
                
                for row in reader:
                    if len(row) < 4:  # Verificar que la fila tiene al menos 4 elementos
                        print(f"Fila ignorada debido a formato incorrecto: {row}")
                        continue

                    origen = row[0].strip()
                    destino = row[1].strip()
                    tipo = row[2].strip()
                    distancia = row[3].strip()


                    # Obtener las ciudades de la red de transporte
                    ciudad_origen = self.red_transporte.get_ciudad(origen)
                    ciudad_destino = self.red_transporte.get_ciudad(destino)

                    if not ciudad_origen:
                        print(f"Error: Ciudad de origen '{origen}' no encontrada. Fila ignorada: {row}")
                        continue
                    if not ciudad_destino:
                        print(f"Error: Ciudad de destino '{destino}' no encontrada. Fila ignorada: {row}")
                        continue

                    # Procesar restricciones si existen
                    tipo_restriccion = row[4].strip() if len(row) > 4 and row[4] else None
                    valor_restriccion = row[5].strip() if len(row) > 5 and row[5] else None

                    # Crear la conexión
                    conexion = Conexion(
                        ciudad_origen,
                        ciudad_destino,
                        distancia,
                        tipo,
                        tipo_restriccion,
                        valor_restriccion
                    )
                    
                    # Agregar la conexión a la red
                    self.red_transporte.agregar_conexion(conexion)

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {archivo_conexiones}")
        except Exception as e:
            print(f"Error al cargar conexiones: {str(e)}")
            