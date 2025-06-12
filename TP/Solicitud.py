from Ciudad import Ciudad

class Solicitud:
    def __init__(self, id_solicitud, peso, ciudad_origen, ciudad_destino):
        """
        Inicializa una solicitud de transporte.
        
        Args:
            id_solicitud (str): Identificador único de la solicitud
            peso (int): Peso de la carga en kilogramos
            ciudad_origen (Ciudad): Ciudad de origen
            ciudad_destino (Ciudad): Ciudad de destino
        """
        self.id_solicitud = id_solicitud
        self.peso = peso
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino

    def __str__(self):
        """Devuelve una representación en string de la solicitud"""
        return f"Solicitud {self.id_solicitud}: {self.peso}kg de {self.ciudad_origen.nombre} a {self.ciudad_destino.nombre}" 