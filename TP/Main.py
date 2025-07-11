from RedTransporte import RedTransporte
from CargaConexiones import CargadorDeConexiones
from CargaSolicitudes import CargadorDeDato
from CargaNodos import CargadorDeNodos
from Ciudad import Ciudad
from Vehiculos import Aereo, Ferroviario, Maritimo, Automotor
from Conexiones import Conexion
from mostrar_mejores_caminos import MostradorCaminos
from graficos import Graficador


def inicializar_red_transporte():
    """Inicializa la red de transporte cargando todos los datos necesarios."""
    # Crear la red de transporte
    red_transporte = RedTransporte()
   
    # 1. Cargar nodos (ciudades)
    print("\n1. Cargando nodos...")
    cargador_nodos = CargadorDeNodos(red_transporte)
    cargador_nodos.cargar_nodos('TP/nodos.csv')

    # 2. Cargar conexiones
    print("\n2. Cargando conexiones...")
    cargador_conexiones = CargadorDeConexiones(red_transporte)
    cargador_conexiones.cargar_conexiones('TP/conexiones.csv')
   
    # 3. Cargar solicitudes
    print("\n3. Cargando solicitudes...")
    cargador_solicitudes = CargadorDeDato(red_transporte)
    cargador_solicitudes.cargar_solicitudes('TP/solicitudes.csv')
   
    return red_transporte

def main():
    """Función principal que coordina la ejecución del programa."""
    try:
        print("=== Sistema de Transporte ===")
       
        # 1. Inicializar red de transporte (cargar archivos en estructuras)
        red_transporte = inicializar_red_transporte()
       
        # 2. Mostrar estadísticas de la red
        red_transporte.mostrar_estadisticas()
       

        # 3. Obtener caminos para las solicitudes
        print("\n=== Procesando solicitudes ===")
        mostrador = MostradorCaminos()
        mostrador.mostrar_mejores_caminos(red_transporte)

        # 4. Mostrar imprevistos de la red
        red_transporte.mostrar_imprevistos()

        print("\n=== Programa finalizado exitosamente ===")
        
    except Exception as e:
        print(f"Error inesperado en el programa: {str(e)}")

if __name__ == "__main__":
    main()

