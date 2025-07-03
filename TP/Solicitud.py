from Ciudad import Ciudad

class Solicitud:
    def __init__(self, id_solicitud, peso, ciudad_origen, ciudad_destino):
        try:
            self.peso = int(peso)  
        except ValueError:
            raise ValueError(f"El peso de la solicitud '{id_solicitud}' no es válido: '{peso}'")
        self.id_solicitud = id_solicitud
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino

    def __str__(self):
        """Devuelve una representación en string de la solicitud"""
        return f"Solicitud {self.id_solicitud}: {self.peso}kg de {self.ciudad_origen.get_nombre()} a {self.ciudad_destino.get_nombre()}" 