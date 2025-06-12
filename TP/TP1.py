from RedTransporte import RedTransporte
from CargaConexiones import CargadorDeConexiones
from CargaSolicitudes import CargadorDeDatos
from CargaNodos import CargadorDeNodos
from Clases import Ciudad
from Vehiculos import Aereo, Ferroviario, Maritimo, Automotor
from Conexiones import Conexion

# Método para obtener las conexiones desde Zarate en Automotor y mostrar la distancia
def obtener_conexiones_desde_zarate_auto(red_transporte):
    # Obtener todas las conexiones de Zarate
    conexiones_zarate_auto = []
    zarate = red_transporte.get_ciudad("Zarate")
    
    if zarate:
        # Filtrar las conexiones desde Zarate que usan el modo "Automotor"
        for conexion in zarate.posibles_conexiones:
            if conexion.tipo_transporte == "Automotor":
                # Agregar las conexiones que cumplen con el filtro
                conexiones_zarate_auto.append(conexion)

        # Mostrar las conexiones encontradas y sus distancias
        if conexiones_zarate_auto:
            print("Conexiones desde Zarate en Automotor:")
            for conexion in conexiones_zarate_auto:
                print(f"{conexion.ciudad2.nombre} - Distancia: {conexion.distancia} km")
        else:
            print("No se encontraron conexiones en Automotor desde Zarate.")
    else:
        print("La ciudad Zarate no está registrada en la red.")

# Crear una instancia de RedTransporte
red_transporte = RedTransporte()

# 2. Crear el cargador de datos para nodos
cargador_nodos = CargadorDeNodos(red_transporte)

# 3. Cargar los nodos desde el archivo CSV
cargador_nodos.cargar_nodos('TP/nodos.csv')

# 2. Crear el cargador de datos para conexiones
cargador_conexiones = CargadorDeConexiones(red_transporte)

# 3. Cargar las conexiones desde el archivo CSV
cargador_conexiones.cargar_conexiones('TP/conexiones.csv')  # Ajusta la ruta del archivo según sea necesario

# Llamar al método para probarlo con la instancia de red_transporte
obtener_conexiones_desde_zarate_auto(red_transporte)

