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
        return list(filter(lambda c: c.tipo_transporte.lower() == tipo_transporte.lower(), self.conexiones))

    def filtrar_conexiones_validas(self, vehiculo):
        """ Filtra las conexiones válidas según el tipo de vehículo y las restricciones """
        return list(filter(lambda conexion: conexion.es_valida_para_vehiculo(vehiculo), self.conexiones))

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

            for conexion in ciudad_obj.posibles_conexiones:
                if not conexion.es_valida_para_vehiculo(vehiculo):
                    continue
                # Determinar la siguiente ciudad en la conexión
                siguiente_ciudad = conexion.ciudad2.nombre if conexion.ciudad1.nombre == ciudad_actual else conexion.ciudad1.nombre
                if siguiente_ciudad not in visitadas:
                    visitadas.add(siguiente_ciudad)
                    camino_actual.append(conexion)
                    dfs(siguiente_ciudad, ciudad_destino, camino_actual, caminos_encontrados, visitadas)
                    camino_actual.pop()
                    visitadas.remove(siguiente_ciudad)

        caminos_encontrados = []
        dfs(origen, destino, [], caminos_encontrados, set([origen]))
        return caminos_encontrados

    def obtener_estadisticas(self):
        """ Devuelve estadísticas básicas de la red de transporte """
        return {
            'total_ciudades': len(self.ciudades),
            'total_conexiones': len(self.conexiones),
            'total_solicitudes': len(self.solicitudes),
            'conexiones_por_tipo': {
                'aerea': len(self.get_conexiones_por_tipo('aerea')),
                'fluvial': len(self.get_conexiones_por_tipo('fluvial')),
                'ferroviaria': len(self.get_conexiones_por_tipo('ferroviaria')),
                'automotor': len(self.get_conexiones_por_tipo('automotor'))
            }
        }

    def _construir_itinerario(self, camino, origen):
        """
        Construye un itinerario ordenado a partir de un camino.
        
        Args:
            camino: Lista de conexiones
            origen: Nombre de la ciudad de origen
            
        Returns:
            list: Lista ordenada de nombres de ciudades
        """
        if not camino:
            return []
            
        # Inicializar el itinerario con la ciudad de origen
        itinerario = [origen]
        ciudad_actual = origen
        
        # Para cada conexión, determinar la siguiente ciudad
        for conexion in camino:
            # Determinar cuál es la siguiente ciudad
            if conexion.ciudad1.nombre == ciudad_actual:
                siguiente = conexion.ciudad2.nombre
            else:
                siguiente = conexion.ciudad1.nombre
                
            itinerario.append(siguiente)
            ciudad_actual = siguiente
            
        return itinerario

    def _construir_tramos(self, camino, vehiculo, solicitud):
        """
        Construye la lista de tramos con la información necesaria para los gráficos.
        
        Args:
            camino: Lista de conexiones
            vehiculo: Vehículo que realizará el viaje
            solicitud: Solicitud de transporte
            
        Returns:
            list: Lista de diccionarios con información de cada tramo
        """
        tramos = []
        cant_vehiculos = (solicitud.peso + vehiculo.capacidad - 1) // vehiculo.capacidad
        
        for conexion in camino:
            # Determinar origen y destino del tramo
            if hasattr(conexion, 'ciudad1') and hasattr(conexion, 'ciudad2'):
                origen = conexion.ciudad1.nombre
                destino = conexion.ciudad2.nombre
            else:
                # Fallback si la conexión no tiene las ciudades definidas
                continue
            
            # Calcular costo del tramo
            costo_fijo = float(vehiculo.costo_fijo) if vehiculo.costo_fijo is not None else 0
            if hasattr(vehiculo, 'calcular_costo_fijo') and vehiculo.costo_fijo is None:
                costo_fijo = float(vehiculo.calcular_costo_fijo(getattr(conexion, 'restriccion', None)))
            
            costo_km = float(vehiculo.costo_km) if vehiculo.costo_km is not None else 0
            if hasattr(vehiculo, 'calcular_costo_por_km') and vehiculo.costo_km is None:
                costo_km = float(vehiculo.calcular_costo_por_km(conexion.distancia))
            
            # Costo del tramo: (costo_fijo + costo_km * distancia) * cant_vehiculos
            costo_tramo = (costo_fijo + costo_km * conexion.distancia) * cant_vehiculos
            
            # Calcular tiempo del tramo
            velocidad = float(vehiculo.velocidad)
            if hasattr(vehiculo, 'calcular_velocidad'):
                if hasattr(conexion, 'tipo_restriccion') and conexion.tipo_restriccion == 'prob_mal_tiempo':
                    velocidad = float(vehiculo.calcular_velocidad(float(conexion.restriccion)))
                else:
                    velocidad = float(vehiculo.calcular_velocidad())
            
            tiempo_tramo = conexion.distancia / velocidad if velocidad > 0 else float('inf')
            tiempo_tramo_minutos = round(tiempo_tramo * 60)  # Convertir a minutos
            
            tramos.append({
                'origen': origen,
                'destino': destino,
                'distancia': conexion.distancia,
                'tiempo': tiempo_tramo_minutos,
                'costo': costo_tramo
            })
        
        return tramos

    def mejores_caminos_para_solicitud(self, solicitud, vehiculos):
        """
        Encuentra los mejores caminos (más barato y más rápido) para una solicitud dada.
        
        Args:
            solicitud: Solicitud de transporte
            vehiculos: Diccionario de vehículos disponibles
            
        Returns:
            dict: Diccionario con los mejores caminos (más barato y más rápido)
        """
        # Listas para almacenar todos los resultados
        todos_resultados = []
        
        # Procesar cada tipo de vehículo
        for tipo_vehiculo, vehiculo in vehiculos.items():
            # Buscar todos los caminos posibles para este tipo de vehículo
            caminos = self.encontrar_caminos_posibles(
                solicitud.ciudad_origen.nombre, 
                solicitud.ciudad_destino.nombre, 
                vehiculo
            )
            
            # Si no hay caminos posibles para este vehículo, continuar con el siguiente
            if not caminos:
                continue
                
            for camino in caminos:
                # Cantidad de vehículos necesaria para la carga (redondeo hacia arriba)
                cant_vehiculos = (solicitud.peso + vehiculo.capacidad - 1) // vehiculo.capacidad
                
                # Cálculo especial para Automotor según la tabla
                if isinstance(vehiculo, Automotor):
                    # Para 70000 kg con capacidad de 30000 kg: necesitamos 3 vehículos
                    # Distribución: 30000 + 30000 + 10000
                    costo_por_kilo = vehiculo.calcular_costo_por_kg(solicitud.peso)
                    costo_vehiculo = solicitud.peso * costo_por_kilo
                else:
                    # Para otros vehículos, usar el cálculo estándar
                    costo_por_kilo = 0
                    if hasattr(vehiculo, 'calcular_costo_por_kg') and vehiculo.costo_kg is None:
                        costo_por_kilo = float(vehiculo.calcular_costo_por_kg(solicitud.peso))
                    else:
                        costo_por_kilo = float(vehiculo.costo_kg) if vehiculo.costo_kg is not None else 0
                    
                    costo_vehiculo = costo_por_kilo * solicitud.peso
                
                # Calcular costo y tiempo para cada tramo
                costo_total_tramos = 0
                tiempo_total = 0
                
                # Construir el itinerario
                itinerario = self._construir_itinerario(camino, solicitud.ciudad_origen.nombre)
                
                for conexion in camino:
                    # Costo fijo por tramo
                    costo_fijo = float(vehiculo.costo_fijo) if vehiculo.costo_fijo is not None else 0
                    if hasattr(vehiculo, 'calcular_costo_fijo') and vehiculo.costo_fijo is None:
                        costo_fijo = float(vehiculo.calcular_costo_fijo(getattr(conexion, 'restriccion', None)))
                    
                    # Costo por km por tramo
                    costo_km = float(vehiculo.costo_km) if vehiculo.costo_km is not None else 0
                    if hasattr(vehiculo, 'calcular_costo_por_km') and vehiculo.costo_km is None:
                        costo_km = float(vehiculo.calcular_costo_por_km(conexion.distancia))
                    
                    # Costo de este tramo: (costo_fijo + costo_km * distancia) * cant_vehiculos
                    costo_tramo = (costo_fijo + costo_km * conexion.distancia) * cant_vehiculos
                    costo_total_tramos += costo_tramo
                    
                    # Velocidad para este tramo
                    velocidad = float(vehiculo.velocidad)
                    if hasattr(vehiculo, 'calcular_velocidad'):
                        if hasattr(conexion, 'tipo_restriccion') and conexion.tipo_restriccion == 'prob_mal_tiempo':
                            velocidad = float(vehiculo.calcular_velocidad(float(conexion.restriccion)))
                        else:
                            velocidad = float(vehiculo.calcular_velocidad())
                    
                    # Tiempo para este tramo (más preciso)
                    tiempo_tramo = conexion.distancia / velocidad if velocidad > 0 else float('inf')
                    tiempo_total += tiempo_tramo
                
                # Costo total para este itinerario: suma de costos por tramo + costo por kilo de la carga
                costo_total = costo_total_tramos + costo_vehiculo
                
                # Convertir tiempo de horas a minutos (redondeado)
                tiempo_total_minutos = round(tiempo_total * 60)
                
                # Crear un itinerario legible
                itinerario_str = " - ".join(itinerario)
                
                # Construir tramos para los gráficos
                tramos = self._construir_tramos(camino, vehiculo, solicitud)
                
                # Agregar este resultado a la lista de todos los resultados
                todos_resultados.append({
                    'camino': camino,
                    'tipo_vehiculo': tipo_vehiculo,
                    'modo': vehiculo.nombre,
                    'itinerario': itinerario_str,
                    'costo_total': costo_total,
                    'tiempo_total': tiempo_total,
                    'tiempo_total_minutos': tiempo_total_minutos,
                    'cant_vehiculos': cant_vehiculos,
                    'tramos': tramos
                })
        
        # Si no hay resultados, retornar None para ambos
        if not todos_resultados:
            return {'mas_barato': None, 'mas_rapido': None}
        
        # Encontrar el camino más barato
        mas_barato = min(todos_resultados, key=lambda x: x['costo_total'])
        
        # Encontrar el camino más rápido
        mas_rapido = min(todos_resultados, key=lambda x: x['tiempo_total'])
        
        return {'mas_barato': mas_barato, 'mas_rapido': mas_rapido}
