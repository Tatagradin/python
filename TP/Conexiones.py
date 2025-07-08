import Vehiculos
from Ciudad import Ciudad
from restricciones import Restricciones

class Conexion:
    
    def __init__(self, ciudad1: Ciudad, ciudad2: Ciudad, distancia, tipo_transporte: str, tipo_restriccion: str = '', restriccion=None):
        try:
            self.distancia = int(distancia)
        except ValueError:
            raise ValueError(f"La distancia ingresada no es válida: '{distancia}'")

        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.tipo_transporte = tipo_transporte if tipo_transporte is not None else ""
        self.tipo_restriccion = tipo_restriccion
        self.restriccion = Restricciones.crear_restriccion_conexion(tipo_restriccion, restriccion)

    def es_valida_para_vehiculo(self, vehiculo: Vehiculos.Vehiculo) -> bool:
        tipo_vehiculo = vehiculo.get_tipo_transporte()
        if tipo_vehiculo is None:
            return False
        tipo_vehiculo = tipo_vehiculo.lower()
        tipo_conexion = self.tipo_transporte.lower()

        if tipo_vehiculo not in Vehiculos.Vehiculo.tipos_validos or tipo_vehiculo != tipo_conexion:
            return False

        if self.restriccion:
            return self.restriccion.es_valida(vehiculo, self)
        return True

    def get_ciudad1(self):
        return self.ciudad1

    def get_ciudad2(self):
        return self.ciudad2

    def get_nombre_ciudad1(self):
        return self.ciudad1.get_nombre()

    def get_nombre_ciudad2(self):
        return self.ciudad2.get_nombre()

    def get_ciudad_opuesta(self, nombre_ciudad):
        if self.ciudad1.get_nombre() == nombre_ciudad:
            return self.ciudad2
        elif self.ciudad2.get_nombre() == nombre_ciudad:
            return self.ciudad1
        return None

    def get_nombres_ciudades(self):
        return (self.ciudad1.get_nombre(), self.ciudad2.get_nombre())

    def get_distancia(self):
        return self.distancia

    def get_tipo_transporte(self):
        return self.tipo_transporte

    def get_tipo_restriccion(self):
        return self.tipo_restriccion

    def get_restriccion(self):
        return self.restriccion