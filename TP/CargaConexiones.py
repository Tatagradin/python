from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *
from RedTransporte import RedTransporte
from leector_csv import Cargador

import csv

class CargadorDeConexiones(Cargador):
    def __init__(self, red_transporte):
        self.red_transporte = red_transporte

    def cargar_conexiones(self, archivo_conexiones):
        """Carga las conexiones desde un archivo CSV y las agrega a la red de transporte."""
        try:
            # Usar función común para leer el archivo
            filas = CargadorDeConexiones.leer_csv_comun(archivo_conexiones)
            
            for row in filas:
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
                tipo_restriccion = row[4].strip() if len(row) > 4 and row[4] else ''
                valor_restriccion = row[5].strip() if len(row) > 5 and row[5] else None

                try:
                    conexion = Conexion(
                        ciudad_origen,
                        ciudad_destino,
                        distancia,
                        tipo,
                        tipo_restriccion,
                        valor_restriccion
                    )
                    self.red_transporte.agregar_conexion(conexion)
                except ValueError as e:
                    print(f"Error al crear conexión entre {origen} y {destino}: {e}")
            
            if len(self.red_transporte.conexiones) == 0:
                raise Exception("No se pudo cargar ninguna conexión. Verifique el archivo conexiones.csv")
                
        except Exception as e:
            raise Exception(f"Error al cargar conexiones: {str(e)}")
            