class Ciudad:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.posibles_conexiones = []  # lista enlazada de conexiones

    def agregar_conexion(self, conexion):
        self.posibles_conexiones.append(conexion)  # agregar al final de la lista


class Conexion:
    def __init__(self, ciudad1: 'Ciudad', ciudad2: 'Ciudad', distancia: int,
                 tipo_transporte: str, tipo_restriccion: str = None, restriccion = None):
        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.distancia = distancia  # en kilometross
        self.tipo_transporte = tipo_transporte  # 'aereo', 'ferroviario', etc.
        self.tipo_restriccion = tipo_restriccion  # 'peso', 'velocidad', etc.
        self.restriccion = restriccion  # valor numérico

    def __str__(self):
        return f"{self.ciudad1.nombre} <-> {self.ciudad2.nombre} por {self.tipo_transporte}"


class Vehiculo:
    def __init__(self, nombre, velocidad, capacidad, costo_fijo, costo_km, costo_kg):
        self.nombre = nombre
        self.velocidad = velocidad        # km/h
        self.capacidad = capacidad        # kg
        self.costo_fijo = costo_fijo      # por tramo
        self.costo_km = costo_km          # por km
        self.costo_kg = costo_kg          # por kg


class Ferroviario(Vehiculo):
    def __init__(self):
        super().__init__("Tren", 100, 150000, 100, 20, 3)

class Automotor(Vehiculo):
    def __init__(self):
        super().__init__("Camión", 80, 30000, 30, 5, 1)

class Maritimo(Vehiculo):
    def __init__(self):
        super().__init__("Barco", 40, 100000, 500, 15, 2)

class Aereo(Vehiculo):
    def __init__(self):
        super().__init__("Avión", 600, 5000, 750, 40, 10)
