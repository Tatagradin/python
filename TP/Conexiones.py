
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