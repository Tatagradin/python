class Ciudad:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.posibles_conexiones = [] 
    def agregar_conexion(self, conexion):
        self.posibles_conexiones.append(conexion)  # agregar al final de la lista

    def get_nombre(self):
        return self.nombre

