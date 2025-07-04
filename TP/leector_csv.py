import csv

def leer_csv_comun(archivo):

    try:
        with open(archivo, mode='r') as file:                        #Función común para leer archivos csv
            reader = csv.reader(file)                                #Devuelve las filas del archivo (sin la cabecera)
            next(reader)  # Saltar la primera fila (cabecera)
            return list(reader)
    except FileNotFoundError:
        raise Exception(f"No se encontró el archivo {archivo}")
    except Exception as e:
        raise Exception(f"Error al leer archivo: {str(e)}") 