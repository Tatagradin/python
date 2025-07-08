class Ciudad:
    def __init__(self, nombre: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la ciudad no puede estar vacío")
        self.nombre = nombre.strip()
        self.posibles_conexiones = [] 
    def agregar_conexion(self, conexion):
        self.posibles_conexiones.append(conexion)  # agregar al final de la lista

    def get_nombre(self):
        return self.nombre

    def get_posibles_conexiones(self):
        return self.posibles_conexiones

