
class Conexion:
    """
    Representa una conexión entre dos ciudades con un tipo específico de transporte.
    
    Attributes:
        ciudad1 (Ciudad): Ciudad de origen
        ciudad2 (Ciudad): Ciudad de destino
        distancia (int): Distancia en kilómetros
        tipo_transporte (str): Tipo de transporte ('Ferroviaria', 'Automotor', 'Fluvial', 'Aerea')
        tipo_restriccion (str, optional): Tipo de restricción ('velocidad_max', 'peso_max', 'tipo', 'prob_mal_tiempo')
        restriccion (str/float, optional): Valor de la restricción
    """
    ""
    def __init__(self, ciudad1: 'Ciudad', ciudad2: 'Ciudad', distancia: int,
                 tipo_transporte: str, tipo_restriccion: str = None, restriccion = None):
        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.distancia = distancia  # en kilómetros
        self.tipo_transporte = tipo_transporte  # 'Ferroviaria', 'Automotor', 'Fluvial', 'Aerea'
        self.tipo_restriccion = tipo_restriccion  # 'velocidad_max', 'peso_max', 'tipo', 'prob_mal_tiempo'
        self.restriccion = restriccion  # valor de la restricción

    def __str__(self):
        """Devuelve una representación en string de la conexión"""
        return f"{self.ciudad1.nombre} <-> {self.ciudad2.nombre} por {self.tipo_transporte}"

    def es_valida_para_vehiculo(self, vehiculo) -> bool:
        """
        Verifica si la conexión es válida para un tipo específico de vehículo.
        
        Args:
            vehiculo: Instancia del vehículo a verificar
            
        Returns:
            bool: True si la conexión es válida para el vehículo, False en caso contrario
        """
        # Mapeo de tipos de vehículos a tipos de conexión
        tipo_mapping = {
            'ferroviaria': 'ferroviaria',
            'automotor': 'automotor',
            'fluvial': 'fluvial',
            'aerea': 'aerea'
        }
        
        # Verificar si el tipo de transporte coincide
        tipo_vehiculo = vehiculo.nombre.lower()
        tipo_conexion = self.tipo_transporte.lower()
        
        if tipo_mapping.get(tipo_vehiculo) != tipo_conexion:
            return False
            
        # Verificar restricciones específicas
        if self.tipo_restriccion == 'velocidad_max':
            # Ferroviario vehicles ignore velocidad_max restrictions
            if tipo_vehiculo == 'ferroviaria':
                pass
            elif hasattr(vehiculo, 'velocidad'):
                return vehiculo.velocidad <= float(self.restriccion)
            
        if self.tipo_restriccion == 'peso_max' and hasattr(vehiculo, 'capacidad'):
            return vehiculo.capacidad <= float(self.restriccion)
            
        if self.tipo_restriccion == 'tipo' and tipo_vehiculo == 'fluvial':
            return self.restriccion in ['fluvial', 'maritimo']
            
        if self.tipo_restriccion == 'prob_mal_tiempo' and tipo_vehiculo == 'aerea':
            return float(self.restriccion) <= 0.3  # Máxima probabilidad aceptable de mal tiempo
            
        return True
