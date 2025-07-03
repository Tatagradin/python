from RedTransporte import RedTransporte
from CargaConexiones import CargadorDeConexiones
from CargaSolicitudes import CargadorDeDatos
from CargaNodos import CargadorDeNodos
from Ciudad import Ciudad
from Vehiculos import Aereo, Ferroviario, Maritimo, Automotor
from Conexiones import Conexion
from mostrar_mejores_caminos import mostrar_mejores_caminos
from graficos import mostrar_graficos_itinerario


def inicializar_red_transporte():

    try:
        # Crear la red de transporte
        red_transporte = RedTransporte()
        
        # 1. Cargar nodos (ciudades)
        print("\n1. Cargando nodos desde nodos.csv...")
        cargador_nodos = CargadorDeNodos(red_transporte)
        cargador_nodos.cargar_nodos('TP/nodos.csv')

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
       
        return red_transporte
        
    except Exception as e:
        print(f"Error al inicializar la red de transporte: {str(e)}")
        return None

def probar_conexiones_desde_ciudad(red_transporte, nombre_ciudad, tipo_vehiculo):
    ciudad = red_transporte.get_ciudad(nombre_ciudad)
    if not ciudad:
        print(f"Error: La ciudad {nombre_ciudad} no está registrada en la red.")
        return
        
    print(f"\nConexiones desde {nombre_ciudad} para {tipo_vehiculo}:")
    conexiones = list(filter(lambda c: c.tipo_transporte.lower() == tipo_vehiculo.lower(), ciudad.posibles_conexiones))
    
    if conexiones:
        for conexion in conexiones:
            ciudad_destino = conexion.get_ciudad2().get_nombre() if conexion.get_ciudad1().get_nombre() == nombre_ciudad else conexion.get_ciudad1().get_nombre()
            print(f"→ {ciudad_destino} - Distancia: {conexion.distancia} km")
    else:
        print(f"No se encontraron conexiones de tipo {tipo_vehiculo} desde {nombre_ciudad}")

def probar_caminos_posibles(red_transporte, origen, destino, vehiculo):
    print(f"\nProbando caminos con {vehiculo.__class__.__name__} ({origen} -> {destino}):")
    caminos = red_transporte.encontrar_caminos_posibles(origen, destino, vehiculo)
    
    if caminos:
        for i, camino in enumerate(caminos, 1):
            print(f"\nCamino {i}:")
            for conexion in camino:
                print(f"  {conexion.get_nombre_ciudad1()} -> {conexion.get_nombre_ciudad2()} ({conexion.tipo_transporte})")
    else:
        print(f"No se encontraron caminos posibles de {origen} a {destino}")

def obtener_tipos_transporte(red_transporte):
    """Obtiene los tipos de transporte únicos de las conexiones"""
    return list(set(c.tipo_transporte.lower() for c in red_transporte.conexiones))
def main():
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

