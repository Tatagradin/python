from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *


class RedTransporte:
    def __init__(self):
        self.ciudades = {}        # Diccionario para almacenar las ciudades por nombre
        self.conexiones = []      # Lista global que guarda todas las conexiones
        self.solicitudes = []     # Lista para almacenar las solicitudes de transporte

    def agregar_ciudad(self, ciudad):
        """ Agrega una ciudad al diccionario de ciudades usando el nombre como clave """
        self.ciudades[ciudad.nombre] = ciudad

    def agregar_conexion(self, conexion):
        """ Agrega una conexión a la red de transporte y la registra en ambas ciudades involucradas """
        # Primero se agrega la conexión a la lista global de la red
        self.conexiones.append(conexion)

        # Luego, se agrega la conexión a las listas locales de las dos ciudades involucradas
        conexion.ciudad1.agregar_conexion(conexion)  # Registra en la ciudad1
        conexion.ciudad2.agregar_conexion(conexion)  # Registra en la ciudad2

    def agregar_solicitud(self, solicitud):
        """ Agrega una solicitud de transporte a la red """
        self.solicitudes.append(solicitud)

    def get_ciudad(self, nombre):
        """ Devuelve el objeto Ciudad por su nombre """
        return self.ciudades.get(nombre)

    def get_conexiones_desde(self, nombre_ciudad):
        """ Devuelve todas las conexiones salientes desde una ciudad """
        ciudad = self.get_ciudad(nombre_ciudad)
        if ciudad:
            return ciudad.posibles_conexiones
        return []

    def get_conexiones_por_tipo(self, tipo_transporte):
        """ Devuelve todas las conexiones de un tipo específico de transporte """
        return [c for c in self.conexiones if c.tipo_transporte.lower() == tipo_transporte.lower()]

    def filtrar_conexiones_validas(self, vehiculo):
        """ Filtra las conexiones válidas según el tipo de vehículo y las restricciones """
        conexiones_validas = []
        for conexion in self.conexiones:
            # Verificamos si el modo de transporte de la conexión es compatible con el vehículo
            if conexion.tipo_transporte.lower() != vehiculo.nombre.lower():
                continue

            # Validamos las restricciones de tipo de transporte o condiciones especiales
            if conexion.tipo_restriccion == "tipo":
                tipo_conexion = conexion.restriccion
                if isinstance(vehiculo, Maritimo) and tipo_conexion not in ["maritimo", "fluvial"]:
                    continue

            if conexion.tipo_restriccion == "prob_mal_tiempo" and isinstance(vehiculo, Aereo):
                if float(conexion.restriccion) > 0:
                    vehiculo.velocidad = 400  # Ajustamos la velocidad si hay mal tiempo

            conexiones_validas.append(conexion)
        return conexiones_validas

    def encontrar_caminos_posibles(self, origen, destino, vehiculo):
        """
        Encuentra todos los caminos posibles entre dos ciudades usando DFS.
        
        Args:
            origen (str): Nombre de la ciudad de origen
            destino (str): Nombre de la ciudad de destino
            vehiculo: Vehículo que realizará el viaje
            
        Returns:
            list: Lista de caminos posibles, donde cada camino es una lista de conexiones
        """
        def dfs(ciudad_actual, ciudad_destino, camino_actual, caminos_encontrados, visitadas):
            if ciudad_actual == ciudad_destino:
                caminos_encontrados.append(camino_actual[:])
                return

            ciudad_obj = self.get_ciudad(ciudad_actual)
            if not ciudad_obj:
                return

            conexiones_validas = self.filtrar_conexiones_validas(vehiculo)
            
            for conexion in conexiones_validas:
                # Determinar la siguiente ciudad en la conexión
                siguiente_ciudad = conexion.ciudad2.nombre if conexion.ciudad1.nombre == ciudad_actual else conexion.ciudad1.nombre
                
                if siguiente_ciudad not in visitadas:
                    visitadas.add(siguiente_ciudad)
                    camino_actual.append(conexion)
                    dfs(siguiente_ciudad, ciudad_destino, camino_actual, caminos_encontrados, visitadas)
                    camino_actual.pop()
                    visitadas.remove(siguiente_ciudad)

        caminos_encontrados = []
        visitadas = {origen}
        dfs(origen, destino, [], caminos_encontrados, visitadas)
        return caminos_encontrados

    def obtener_estadisticas(self):
        """ Devuelve estadísticas básicas de la red de transporte """
        return {
            'total_ciudades': len(self.ciudades),
            'total_conexiones': len(self.conexiones),
            'total_solicitudes': len(self.solicitudes),
            'conexiones_por_tipo': {
                'aereo': len(self.get_conexiones_por_tipo('aereo')),
                'maritimo': len(self.get_conexiones_por_tipo('maritimo')),
                'ferroviario': len(self.get_conexiones_por_tipo('ferroviario'))
            }
        }

    def mejores_caminos_para_solicitud(self, solicitud, vehiculos):
        """
        Calcula el mejor camino para una solicitud, devolviendo el más barato y el más rápido.
        Args:
            solicitud (Solicitud): La solicitud de transporte
            vehiculos (dict): Diccionario de instancias de vehículos por tipo
        Returns:
            dict: {'mas_barato': {...}, 'mas_rapido': {...}}
        """
        resultados = []
        for tipo, vehiculo in vehiculos.items():
            caminos = self.encontrar_caminos_posibles(solicitud.ciudad_origen.nombre, solicitud.ciudad_destino.nombre, vehiculo)
            for camino in caminos:
                total_distancia = sum(conexion.distancia for conexion in camino)
                # Cantidad de vehículos necesarios
                cant_vehiculos = -(-solicitud.peso // vehiculo.capacidad)  # Redondeo hacia arriba
                # Cálculo de costos y tiempo
                costo_tramos = 0
                for conexion in camino:
                    # Costo fijo y por km
                    if hasattr(vehiculo, 'calcular_costo_por_km') and vehiculo.costo_km is None:
                        costo_km = vehiculo.calcular_costo_por_km(conexion.distancia)
                    else:
                        costo_km = vehiculo.costo_km
                    if hasattr(vehiculo, 'calcular_costo_fijo') and vehiculo.costo_fijo is None:
                        costo_fijo = vehiculo.calcular_costo_fijo(getattr(conexion, 'restriccion', None))
                    else:
                        costo_fijo = vehiculo.costo_fijo
                    costo_tramo = (costo_fijo if costo_fijo else 0) + (costo_km if costo_km else 0) * conexion.distancia
                    costo_tramos += costo_tramo
                costo_tramos *= cant_vehiculos
                # Costo por kilo
                if hasattr(vehiculo, 'calcular_costo_por_kg') and vehiculo.costo_kg is None:
                    costo_kg = vehiculo.calcular_costo_por_kg(solicitud.peso)
                else:
                    costo_kg = vehiculo.costo_kg
                costo_vehiculo = (costo_kg if costo_kg else 0) * solicitud.peso
                costo_total = costo_tramos + costo_vehiculo
                # Tiempo total
                velocidad = vehiculo.velocidad
                if hasattr(vehiculo, 'calcular_velocidad'):
                    velocidad = vehiculo.calcular_velocidad(getattr(conexion, 'restriccion', None))
                tiempo_total = total_distancia / velocidad if velocidad else float('inf')
                resultados.append({
                    'camino': camino,
                    'tipo_vehiculo': tipo,
                    'costo_total': costo_total,
                    'tiempo_total': tiempo_total
                })
        # Elegir el más barato y el más rápido
        mas_barato = min(resultados, key=lambda x: x['costo_total']) if resultados else None
        mas_rapido = min(resultados, key=lambda x: x['tiempo_total']) if resultados else None
        return {'mas_barato': mas_barato, 'mas_rapido': mas_rapido}