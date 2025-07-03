import Vehiculos
from Ciudad import Ciudad
class Conexion:

    def __init__(self, ciudad1: Ciudad, ciudad2: Ciudad, distancia: int,
                 tipo_transporte: str, tipo_restriccion: str = '', restriccion = None):
        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.distancia = Conexion.convertir_distancia(distancia)  # en kilómetros
        self.tipo_transporte = tipo_transporte if tipo_transporte is not None else ""  # asegurar str
        self.tipo_restriccion = tipo_restriccion  # 'velocidad_max', 'peso_max', 'tipo', 'prob_mal_tiempo'
        self.restriccion = restriccion  # valor de la restricción

    @staticmethod
    def convertir_distancia(valor):
        try:
            return int(valor)
        except (ValueError):
            print("La distancia cargada en el archivo debe ser un número entero")
            return None

    def es_valida_para_vehiculo(self, vehiculo: Vehiculos.Vehiculo) -> bool:
        tipo_vehiculo = vehiculo.get_tipo_transporte()
        if tipo_vehiculo is None:
            return False
        tipo_vehiculo = tipo_vehiculo.lower()
        tipo_conexion = self.tipo_transporte.lower()

        if tipo_vehiculo not in Vehiculos.Vehiculo.tipos_validos or tipo_vehiculo != tipo_conexion:
            return False

        # Verificar restricciones específicas
        if self.tipo_restriccion == 'velocidad_max':
            # Ferroviario ignora velocidad_max
            if tipo_vehiculo == 'ferroviaria':
                pass
            else:
                velocidad = vehiculo.get_velocidad_maxima()
                if self.restriccion is None:
                    return False
                return velocidad <= float(self.restriccion)

        if self.tipo_restriccion == 'peso_max':
            capacidad = vehiculo.get_capacidad()
            if self.restriccion is None:
                return False
            return capacidad <= float(self.restriccion)

        if self.tipo_restriccion == 'tipo' and tipo_vehiculo == 'fluvial':
            return self.restriccion in ['fluvial', 'maritimo']

        if self.tipo_restriccion == 'prob_mal_tiempo' and tipo_vehiculo == 'aerea':
            if self.restriccion is None:
                return False
            return float(self.restriccion) <= 0.3
        return True

    def get_ciudad1(self):
        return self.ciudad1

    def get_ciudad2(self):
        return self.ciudad2

    def get_nombre_ciudad1(self):
        return self.ciudad1.nombre

    def get_nombre_ciudad2(self):
        return self.ciudad2.nombre

    def get_ciudad_opuesta(self, nombre_ciudad):
        if self.ciudad1.nombre == nombre_ciudad:
            return self.ciudad2
        elif self.ciudad2.nombre == nombre_ciudad:
            return self.ciudad1
        return None

    def get_nombres_ciudades(self):
        return (self.ciudad1.nombre, self.ciudad2.nombre)