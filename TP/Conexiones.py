import Vehiculos
class Conexion:


    def __init__(self, ciudad1: 'Ciudad', ciudad2: 'Ciudad', distancia: int,
                 tipo_transporte: str, tipo_restriccion: str = None, restriccion = None):
        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.distancia = Conexion.convertir_distancia(distancia)  # en kilómetros
        self.tipo_transporte = tipo_transporte  # 'Ferroviaria', 'Automotor', 'Fluvial', 'Aerea'
        self.tipo_restriccion = tipo_restriccion  # 'velocidad_max', 'peso_max', 'tipo', 'prob_mal_tiempo'
        self.restriccion = restriccion  # valor de la restricción

    @staticmethod
    def convertir_distancia(valor):

        try:
            return int(valor)          # éxito → devolvemos el int
        except (ValueError):
            # Propagamos un mensaje más claro sin imprimir nada
            print("La distancia cargada en el archivo debe ser un número entero")
            return None

    def es_valida_para_vehiculo(self, vehiculo) -> bool:

        # Verificar si el tipo de transporte coincide
        tipo_vehiculo = vehiculo.nombre.lower()
        tipo_conexion = self.tipo_transporte.lower()

       

        if tipo_vehiculo not in Vehiculos.tipos_validos or tipo_vehiculo != tipo_conexion:
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
