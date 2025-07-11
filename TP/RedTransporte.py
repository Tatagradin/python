from Conexiones import Conexion
from Ciudad import Ciudad
from Vehiculos import *

from Solicitud import Solicitud
import random

class RedTransporte:
    
    def __init__(self):
        self.ciudades = {}        # Diccionario para almacenar las ciudades por nombre
        self.conexiones = []      # Lista global que guarda todas las conexiones
        self.solicitudes = []     # Lista para almacenar las solicitudes de transporte
        self.pila_imprevistos = []  # Pila para almacenar imprevistos

    def agregar_ciudad(self, ciudad):
        #Agrega una ciudad al diccionario de ciudades usando el nombre como clave
        self.ciudades[ciudad.get_nombre()] = ciudad

    def agregar_conexion(self, conexion):
        #Agrega una conexión a la red de transporte y la registra en ambas ciudades involucradas 
        self.conexiones.append(conexion)
        conexion.get_ciudad1().agregar_conexion(conexion)
        conexion.get_ciudad2().agregar_conexion(conexion)

    def agregar_solicitud(self, solicitud):
        #Agrega una solicitud de transporte a la red 
        self.solicitudes.append(solicitud)

    def get_solicitud(self):
        return self.solicitudes

    def get_ciudad(self, nombre):
        return self.ciudades.get(nombre)

    def get_conexiones(self):
        return self.conexiones

    def get_conexiones_desde(self, nombre_ciudad):
        #Devuelve todas las conexiones salientes desde una ciudad 
        ciudad = self.get_ciudad(nombre_ciudad)
        if ciudad:
            return ciudad.get_posibles_conexiones()
        return []

    def get_conexiones_por_tipo(self, tipo_transporte):
        """ Devuelve todas las conexiones de un tipo específico de transporte """
        return list(filter(lambda c: c.get_tipo_transporte().lower() == tipo_transporte.lower(), self.conexiones))

    def filtrar_conexiones_validas(self, vehiculo):
        """ Filtra las conexiones válidas según el tipo de vehículo y las restricciones """
        return list(filter(lambda conexion: conexion.es_valida_para_vehiculo(vehiculo) and conexion.esta_habilitada(), self.conexiones))

    def encontrar_caminos_posibles(self, origen, destino, vehiculo):
    
        def dfs(ciudad_actual, ciudad_destino, camino_actual, caminos_encontrados, visitadas):
            if ciudad_actual == ciudad_destino:
                caminos_encontrados.append(camino_actual[:])
                return

            ciudad_obj = self.get_ciudad(ciudad_actual)
            if not ciudad_obj:
                return

            for conexion in filter(lambda c: self.conexion_esta_disponible(c, vehiculo), ciudad_obj.get_posibles_conexiones()):
                siguiente_ciudad = conexion.get_ciudad_opuesta(ciudad_actual).get_nombre()
                if siguiente_ciudad not in visitadas:
                    visitadas.add(siguiente_ciudad)
                    camino_actual.append(conexion)
                    dfs(siguiente_ciudad, ciudad_destino, camino_actual, caminos_encontrados, visitadas)
                    camino_actual.pop()
                    visitadas.remove(siguiente_ciudad)

        caminos_encontrados = []
        dfs(origen, destino, [], caminos_encontrados, set([origen]))
        return caminos_encontrados

    def conexion_esta_disponible(self, conexion, vehiculo):
        ciudad1 = conexion.get_nombre_ciudad1()
        ciudad2 = conexion.get_nombre_ciudad2()

        # paro es LIFO
        if vehiculo.get_probabilidad_paro() is not None:
            if random.random() < vehiculo.get_probabilidad_paro():
                mensaje = f"  Paro detectado en el sector {vehiculo.get_nombre().upper()} — Conexión entre {ciudad1} y {ciudad2} inhabilitada."
                self.pila_imprevistos.append(("paro", vehiculo.get_nombre(), ciudad1, ciudad2, mensaje))
                return False

    #corte lifo
        if vehiculo.get_probabilidad_corte() is not None:
            if random.random() < vehiculo.get_probabilidad_corte():
                mensaje = f"  Corte de ruta en transporte {vehiculo.get_nombre().upper()} — Conexión entre {ciudad1} y {ciudad2} inhabilitada."
                self.pila_imprevistos.append(("corte", vehiculo.get_nombre(), ciudad1, ciudad2, mensaje))
                return False

  
        return conexion.es_valida_para_vehiculo(vehiculo)

    def get_cantidad_ciudades(self):
        return len(self.ciudades)

    def obtener_estadisticas(self):
        """ Devuelve estadísticas básicas de la red de transporte """
        return {
            'total_ciudades': self.get_cantidad_ciudades(),
            'total_conexiones': len(self.get_conexiones()),
            'total_solicitudes': len(self.get_solicitud()),
            'conexiones_por_tipo': {
                'aerea': len(self.get_conexiones_por_tipo('aerea')),
                'fluvial': len(self.get_conexiones_por_tipo('fluvial')),
                'ferroviaria': len(self.get_conexiones_por_tipo('ferroviaria')),
                'automotor': len(self.get_conexiones_por_tipo('automotor'))
            }
        }

    def _construir_itinerario(self, camino, origen):

        if not camino:
            return []
            
        # Inicializar el itinerario con la ciudad de origen
        itinerario = [origen]
        ciudad_actual = origen
        
        # Para cada conexión, determinar la siguiente ciudad
        for conexion in camino:
            # Determinar cuál es la siguiente ciudad
            siguiente = conexion.get_ciudad_opuesta(ciudad_actual).get_nombre()
            itinerario.append(siguiente)
            ciudad_actual = siguiente
            
        return itinerario

    def calcular_costo_fijo(self, vehiculo, conexion):
        return vehiculo.calcular_costo_fijo(conexion)

    def _calcular_costo_km(self, vehiculo, conexion):
        return vehiculo.calcular_costo_km(conexion)

    def _calcular_velocidad(self, vehiculo, conexion):
        return vehiculo.calcular_velocidad(conexion)

    def _construir_tramos(self, camino, vehiculo, solicitud):
        tramos = []
        cant_vehiculos = (solicitud.get_peso() + vehiculo.get_capacidad() - 1) // vehiculo.get_capacidad()
        for conexion in camino:
            origen = conexion.get_nombre_ciudad1()
            destino = conexion.get_nombre_ciudad2()
            costo_fijo = self.calcular_costo_fijo(vehiculo, conexion)
            costo_km = self._calcular_costo_km(vehiculo, conexion)
            costo_tramo = (costo_fijo + costo_km * conexion.get_distancia()) * cant_vehiculos
            velocidad = self._calcular_velocidad(vehiculo, conexion)
            tiempo_tramo = conexion.get_distancia() / velocidad if velocidad > 0 else float('inf')
            tiempo_tramo_minutos = round(tiempo_tramo * 60)
            tramos.append({
                'origen': origen,
                'destino': destino,
                'distancia': conexion.get_distancia(),
                'tiempo': tiempo_tramo_minutos,
                'costo': costo_tramo
            })
        return tramos

    def mejores_caminos_para_solicitud(self, solicitud, vehiculos):
        todos_resultados = []
        for tipo_vehiculo, vehiculo in vehiculos.items():
            caminos = self.encontrar_caminos_posibles(
                solicitud.ciudad_origen.get_nombre(), 
                solicitud.ciudad_destino.get_nombre(), 
                vehiculo
            )
            if not caminos:
                continue
            for camino in caminos:
                cant_vehiculos = (solicitud.get_peso() + vehiculo.get_capacidad() - 1) // vehiculo.get_capacidad()
                costo_por_kilo = vehiculo.calcular_costo_por_kg(solicitud.get_peso())
                costo_vehiculo = costo_por_kilo * solicitud.get_peso()
                costo_total_tramos = 0
                tiempo_total = 0
                itinerario = self._construir_itinerario(camino, solicitud.ciudad_origen.get_nombre())
                for conexion in camino:
                    costo_fijo = self.calcular_costo_fijo(vehiculo, conexion)
                    costo_km = self._calcular_costo_km(vehiculo, conexion)
                    costo_tramo = (costo_fijo + costo_km * conexion.get_distancia()) * cant_vehiculos
                    costo_total_tramos += costo_tramo
                    velocidad = self._calcular_velocidad(vehiculo, conexion)
                    tiempo_tramo = conexion.get_distancia() / velocidad if velocidad > 0 else float('inf')
                    tiempo_total += tiempo_tramo
                costo_total = costo_total_tramos + costo_vehiculo
                tiempo_total_minutos = round(tiempo_total * 60)
                itinerario_str = " - ".join(itinerario)
                tramos = self._construir_tramos(camino, vehiculo, solicitud)
                todos_resultados.append({
                    'camino': camino,
                    'tipo_vehiculo': tipo_vehiculo,
                    'modo': vehiculo.get_nombre(),
                    'itinerario': itinerario_str,
                    'costo_total': costo_total,
                    'tiempo_total': tiempo_total,
                    'tiempo_total_minutos': tiempo_total_minutos,
                    'cant_vehiculos': cant_vehiculos,
                    'tramos': tramos
                })
        if not todos_resultados:
            return {'mas_barato': None, 'mas_rapido': None}
        mas_barato = min(todos_resultados, key=lambda x: x['costo_total'])
        mas_rapido = min(todos_resultados, key=lambda x: x['tiempo_total'])
        return {'mas_barato': mas_barato, 'mas_rapido': mas_rapido}
    
    def mostrar_estadisticas(self):
        print("\n=== Estadísticas de la red ===")
        stats = self.obtener_estadisticas()
        print(f"Total de ciudades: {stats['total_ciudades']}")
        print(f"Total de conexiones: {stats['total_conexiones']}")
        print(f"Total de solicitudes: {stats['total_solicitudes']}")
        print("\nConexiones por tipo:")
        for tipo, cantidad in stats['conexiones_por_tipo'].items():
            print(f"- {tipo}: {cantidad}")
    def mostrar_imprevistos(self):
        if self.pila_imprevistos:
            print("\n=== IMPREVISTOS DETECTADOS (orden LIFO) ===")
            while self.pila_imprevistos:
                evento = self.pila_imprevistos.pop()
                print(f"- {evento[-1]}")  