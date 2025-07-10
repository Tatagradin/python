
class Vehiculo:
    tipos_validos = {'ferroviaria', 'automotor', 'maritimo', 'aerea'}

    def __init__(self, nombre, velocidad, capacidad, costo_fijo, costo_km, costo_kg, prob_paro, prob_corte):
        self.nombre = nombre
        self.velocidad = velocidad        # km/h
        self.capacidad = capacidad        # kg
        self.costo_fijo = costo_fijo      # por tramo
        self.costo_km = costo_km          # por km
        self.costo_kg = costo_kg          # por kg
        self.prob_corte = prob_corte      # probabilidad de corte de ruta
        self.prob_paro = prob_paro        # probabilidad de paro del vehiculo

    def get_tipo_transporte(self):
        return self.nombre.lower()

    def get_velocidad_maxima(self):
        return self.velocidad

    def get_capacidad(self):
        return self.capacidad

    def get_nombre(self):
        return self.nombre

    def get_costo_fijo(self):
        return self.costo_fijo
    
    def get_probabilidad_paro(self):
        return self.prob_paro

    def get_probabilidad_corte(self):
        return self.prob_corte

    def get_costo_km(self):
        return self.costo_km

    def calcular_costo_fijo(self, conexion):
        return float(self.costo_fijo)

    def calcular_costo_km(self, conexion):
        return float(self.costo_km)

    def calcular_velocidad(self, conexion):
        return float(self.velocidad)

    def calcular_costo_por_kg(self, peso_total):
        return float(self.costo_kg or 0)

class Ferroviario(Vehiculo):
    def __init__(self):
        super().__init__("ferroviaria", 100, 150000, 100, None, 3, 0.15, 0.10)

    def calcular_costo_km(self, conexion):
        distancia = conexion.get_distancia()
        return 20 if distancia < 200 else 15


class Automotor(Vehiculo):
    def __init__(self):
        super().__init__("automotor", 80, 30000, 30, 5, None, None, 0.25)

    def calcular_costo_por_kg(self, peso_total):
        if peso_total <= 0:
            return 0
            
        capacidad_vehiculo = self.capacidad  # 30000 kg
        
        # Calcular cuántos vehículos completos necesitamos
        vehiculos_completos = peso_total // capacidad_vehiculo
        peso_restante = peso_total % capacidad_vehiculo
        
        # Costo para vehículos completos (a $2.00/kg)
        costo_vehiculos_completos = vehiculos_completos * capacidad_vehiculo * 2.0
        
        # Costo para el vehículo parcial (a $1.00/kg)
        costo_vehiculo_parcial = peso_restante * 1.0 if peso_restante > 0 else 0
        
        # Costo total
        costo_total = costo_vehiculos_completos + costo_vehiculo_parcial
        
        # Retornar costo promedio por kg
        return costo_total / peso_total


class Maritimo(Vehiculo):
    def __init__(self):
        super().__init__("maritimo", 40, 100000, None, 15, 2.0, 0.1, None)

    def calcular_costo_fijo(self, conexion):
        tipo = conexion.get_restriccion()
        if tipo == "fluvial":
            return 500
        elif tipo == "maritimo":
            return 1500
        return 500


class Aereo(Vehiculo):
    def __init__(self):
        super().__init__("aerea", 600, 5000, 750, 40, 10, 0.3, None)

    def calcular_velocidad(self, conexion):
        if conexion.get_tipo_restriccion() == 'prob_mal_tiempo':
            prob = float(conexion.get_restriccion())
            if prob > 0:
                return 400
        return self.velocidad