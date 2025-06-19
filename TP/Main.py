from RedTransporte import RedTransporte
from CargaConexiones import CargadorDeConexiones
from CargaSolicitudes import CargadorDeDatos
from CargaNodos import CargadorDeNodos
from Ciudad import Ciudad
from Vehiculos import Aereo, Ferroviario, Maritimo, Automotor
from Conexiones import Conexion
from mostrar_mejores_caminos import mostrar_mejores_caminos
from graficos import graficar_conexiones_por_tipo

def inicializar_red_transporte():
    """
    Inicializa la red de transporte cargando nodos, conexiones y solicitudes desde archivos CSV.
    
    Returns:
        RedTransporte: Instancia de la red de transporte inicializada
    """
    try:
        # Crear la red de transporte
        red_transporte = RedTransporte()
        
        # 1. Cargar nodos (ciudades)
        print("\n1. Cargando nodos desde nodos.csv...")
        cargador_nodos = CargadorDeNodos(red_transporte)
        cargador_nodos.cargar_nodos('TP/nodos.csv')
        num_ciudades = len(red_transporte.ciudades)
        if num_ciudades == 0:
            raise Exception("No se pudieron cargar las ciudades. Verifique el archivo nodos.csv")
        print(f"✓ Nodos cargados: {num_ciudades} ciudades")
        
        # 2. Cargar conexiones
        print("\n2. Cargando conexiones desde conexiones.csv...")
        cargador_conexiones = CargadorDeConexiones(red_transporte)
        cargador_conexiones.cargar_conexiones('TP/conexiones.csv')
        num_conexiones = len(red_transporte.conexiones)
        if num_conexiones == 0:
            raise Exception("No se pudieron cargar las conexiones. Verifique el archivo conexiones.csv")
        print(f"✓ Conexiones cargadas: {num_conexiones} conexiones")
        
        # 3. Cargar solicitudes
        print("\n3. Cargando solicitudes desde solicitudes.csv...")
        cargador_solicitudes = CargadorDeDatos(red_transporte)
        cargador_solicitudes.cargar_solicitudes('TP/solicitudes.csv')
        num_solicitudes = len(red_transporte.solicitudes)
        if num_solicitudes == 0:
            raise Exception("No se pudieron cargar las solicitudes. Verifique el archivo solicitudes.csv")
        print(f"✓ Solicitudes cargadas: {num_solicitudes} solicitudes")
        
        return red_transporte
        
    except Exception as e:
        print(f"Error al inicializar la red de transporte: {str(e)}")
        return None

def probar_conexiones_desde_ciudad(red_transporte, nombre_ciudad, tipo_vehiculo):
    """
    Prueba y muestra las conexiones disponibles desde una ciudad específica para un tipo de vehículo.
    
    Args:
        red_transporte (RedTransporte): Instancia de la red de transporte
        nombre_ciudad (str): Nombre de la ciudad de origen
        tipo_vehiculo (str): Tipo de vehículo a probar
    """
    ciudad = red_transporte.get_ciudad(nombre_ciudad)
    if not ciudad:
        print(f"Error: La ciudad {nombre_ciudad} no está registrada en la red.")
        return
        
    print(f"\nConexiones desde {nombre_ciudad} para {tipo_vehiculo}:")
    conexiones = [c for c in ciudad.posibles_conexiones if c.tipo_transporte.lower() == tipo_vehiculo.lower()]
    
    if conexiones:
        for conexion in conexiones:
            ciudad_destino = conexion.ciudad2.nombre if conexion.ciudad1.nombre == nombre_ciudad else conexion.ciudad1.nombre
            print(f"→ {ciudad_destino} - Distancia: {conexion.distancia} km")
    else:
        print(f"No se encontraron conexiones de tipo {tipo_vehiculo} desde {nombre_ciudad}")

def probar_caminos_posibles(red_transporte, origen, destino, vehiculo):
    """
    Prueba y muestra los caminos posibles entre dos ciudades para un vehículo específico.
    
    Args:
        red_transporte (RedTransporte): Instancia de la red de transporte
        origen (str): Nombre de la ciudad de origen
        destino (str): Nombre de la ciudad de destino
        vehiculo: Instancia del vehículo a utilizar
    """
    print(f"\nProbando caminos con {vehiculo.__class__.__name__} ({origen} -> {destino}):")
    caminos = red_transporte.encontrar_caminos_posibles(origen, destino, vehiculo)
    
    if caminos:
        for i, camino in enumerate(caminos, 1):
            print(f"\nCamino {i}:")
            for conexion in camino:
                print(f"  {conexion.ciudad1.nombre} -> {conexion.ciudad2.nombre} ({conexion.tipo_transporte})")
    else:
        print(f"No se encontraron caminos posibles de {origen} a {destino}")

def obtener_tipos_transporte(red_transporte):
    """Obtiene los tipos de transporte únicos de las conexiones"""
    return list(set(c.tipo_transporte.lower() for c in red_transporte.conexiones))
def main():
    """
    Función principal que ejecuta el programa.
    """
    try:
        print("=== Iniciando sistema de transporte ===")
        
        # Inicializar red de transporte
        red_transporte = inicializar_red_transporte()
        if not red_transporte:
            print("No se pudo inicializar la red de transporte. Finalizando programa.")
            return
            
        # Obtener tipos de transporte disponibles
        tipos_transporte = obtener_tipos_transporte(red_transporte)
        print(f"\nTipos de transporte disponibles: {', '.join(tipos_transporte)}")
        
        # Mostrar estadísticas de la red
        print("\n=== Estadísticas de la red ===")
        stats = red_transporte.obtener_estadisticas()
        print(f"Total de ciudades: {stats['total_ciudades']}")
        print(f"Total de conexiones: {stats['total_conexiones']}")
        print(f"Total de solicitudes: {stats['total_solicitudes']}")
        print("\nConexiones por tipo:")
        graficar_conexiones_por_tipo(stats)
        for tipo, cantidad in stats['conexiones_por_tipo'].items():
            print(f"- {tipo}: {cantidad}")
        
        # Mostrar mejores caminos para cada solicitud
        vehiculos = {
            'aereo': Aereo(),
            'maritimo': Maritimo(),
            'ferroviario': Ferroviario(),
            'automotor': Automotor()
        }
        mostrar_mejores_caminos(red_transporte, vehiculos)
        
        print("\n=== Programa finalizado exitosamente ===")
        
    except Exception as e:
        print(f"Error inesperado en el programa: {str(e)}")

if __name__ == "__main__":
    main()

