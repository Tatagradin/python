
class Vehiculo:
    tipos_validos = {'ferroviaria', 'automotor', 'fluvial', 'aerea'}

    def _init_(self, nombre, velocidad, capacidad, costo_fijo, costo_km, costo_kg):
        self.nombre = nombre
        self.velocidad = velocidad        # km/h
        self.capacidad = capacidad        # kg
        self.costo_fijo = costo_fijo      # por tramo
        self.costo_km = costo_km          # por km
        self.costo_kg = costo_kg          # por kg

    def get_tipo_transporte(self):
        return self.nombre.lower()

    def get_velocidad_maxima(self):
        return self.velocidad

    def get_capacidad(self):
        return self.capacidad

    def get_nombre(self):
        return self.nombre


class Ferroviario(Vehiculo):
    def _init_(self):
        super()._init_("ferroviaria", 100, 150000, 100, None, 3)

    def calcular_costo_por_km(self, distancia):
        # Según la tabla: $20 para distancias < 200km, $15 para >= 200km
        return 20 if distancia < 200 else 15

    # Si se quiere, se puede sobrescribir get_tipo_transporte
    # def get_tipo_transporte(self):
    #     return "ferroviaria"


class Automotor(Vehiculo):
    def _init_(self):
        super()._init_("automotor", 80, 30000, 30, 5, None)

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

    # def get_tipo_transporte(self):
    #     return "automotor"


class Maritimo(Vehiculo):
    def _init_(self):
        super()._init_("fluvial", 40, 100000, None, 15, 2.0)

    def calcular_costo_fijo(self, tipo):
        # Según la tabla: $500 para fluvial, $1500 para marítimo
        if tipo == "fluvial":
            return 500
        elif tipo == "maritimo":
            return 1500
        return 500  # Default a fluvial

    # def get_tipo_transporte(self):
    #     return "fluvial"


class Aereo(Vehiculo):
    def _init_(self):
        super()._init_("aerea", 600, 5000, 750, 40, 10)

    def calcular_velocidad(self, prob_mal_tiempo=None):
        if prob_mal_tiempo is not None and prob_mal_tiempo > 0:
            return 400
        return self.velocidad