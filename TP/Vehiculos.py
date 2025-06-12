class Vehiculo:
    def __init__(self, nombre, velocidad, capacidad, costo_fijo, costo_km, costo_kg):
        self.nombre = nombre
        self.velocidad = velocidad        # km/h
        self.capacidad = capacidad        # kg
        self.costo_fijo = costo_fijo      # por tramo
        self.costo_km = costo_km          # por km
        self.costo_kg = costo_kg          # por kg


# Subclases corregidas según los criterios definitivos

class Ferroviario(Vehiculo):
    def __init__(self):
        super().__init__("Ferroviaria", 100, 150000, 100, None, 3)  # todo fijo excepto costo por km

    def calcular_costo_por_km(self, distancia):
        return 20 if distancia < 200 else 15


class Automotor(Vehiculo):
    def __init__(self):
        super().__init__("Automotor", 80, 30000, 30, 5, None)  # todo fijo excepto costo por kg

    def calcular_costo_por_kg(self, peso):
        return 1 if peso < 15000 else 2


class Maritimo(Vehiculo):
    def __init__(self):
        super().__init__("Fluvial", 40, 100000, None, 15, 2)  # todo fijo excepto costo fijo

    def calcular_costo_fijo(self, tipo):
        if tipo == "fluvial":
            return 500
        elif tipo == "maritimo":
            return 1500
        return 0


class Aereo(Vehiculo):
    def __init__(self):
        super().__init__("Aerea", 600, 5000, 750, 40, 10)  # todo fijo excepto velocidad

    def calcular_velocidad(self, prob_mal_tiempo=None):
        if prob_mal_tiempo is not None and prob_mal_tiempo > 0:
            return 400
        return self.velocidad
