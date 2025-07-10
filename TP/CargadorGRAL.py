import csv

class Cargador:
    def __init__(self, red_transporte):
        self.red_transporte = red_transporte

    @staticmethod
    def leer_csv_comun(archivo):
        try:
            with open(archivo, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                return list(reader)
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo {archivo}")
        except Exception as e:
            raise Exception(f"Error al leer archivo: {str(e)}")
