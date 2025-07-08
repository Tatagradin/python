class Restriccion:
    def es_valida(self, vehiculo, conexion):
        return True  # Por defecto, sin restricción

class RestriccionVelocidadMax(Restriccion):
    def __init__(self, valor):
        self.valor = float(valor) if valor is not None else None

    def es_valida(self, vehiculo, conexion):
        if self.valor is None:
            return False
        if vehiculo.get_tipo_transporte() == 'ferroviaria':
            return True
        velocidad = vehiculo.get_velocidad_maxima()
        return velocidad <= self.valor

class RestriccionPesoMax(Restriccion):
    def __init__(self, valor):
        self.valor = float(valor) if valor is not None else None

    def es_valida(self, vehiculo, conexion):
        if self.valor is None:
            return False
        capacidad = vehiculo.get_capacidad()
        return capacidad <= self.valor

class RestriccionTipo(Restriccion):
    def __init__(self, valor):
        self.valor = valor

    def es_valida(self, vehiculo, conexion):
        # Solo aplica para fluvial
        if vehiculo.get_tipo_transporte() == 'fluvial':
            return self.valor in ['fluvial', 'maritimo']
        return True

class RestriccionProbMalTiempo(Restriccion):
    def __init__(self, valor):
        self.valor = float(valor) if valor is not None else None

    def es_valida(self, vehiculo, conexion):
        # Solo aplica para aerea
        if vehiculo.get_tipo_transporte() == 'aerea':
            if self.valor is None:
                return False
            return self.valor <= 0.3
        return True

class Restricciones:
    @staticmethod
    def crear_restriccion_conexion(tipo, valor):
        if tipo == 'velocidad_max':
            return RestriccionVelocidadMax(valor)
        if tipo == 'peso_max':
            return RestriccionPesoMax(valor)
        if tipo == 'tipo':
            return RestriccionTipo(valor)
        if tipo == 'prob_mal_tiempo':
            return RestriccionProbMalTiempo(valor)
        return None
