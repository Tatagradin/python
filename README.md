
# Sistema de Transporte - Trabajo Práctico

## Objetivo del Proyecto
Este proyecto tiene como objetivo simular un sistema de transporte multimodal en la Provincia de Buenos Aires, utilizando programación orientada a objetos. El sistema permite procesar solicitudes de carga y generar itinerarios óptimos que minimicen:
- Tiempo total de entrega (KPI 1)
- Costo total del transporte (KPI 2)

## Estructura del Código
El código se organiza en módulos separados según su responsabilidad:

- `Main.py`: Programa principal que inicializa la red, carga archivos y ejecuta la planificación.
- `RedTransporte.py`: Clase central que gestiona nodos, conexiones y solicitudes.
- `Ciudad.py`: Define los nodos (ciudades).
- `Conexiones.py`: Representa las rutas entre ciudades, incluyendo restricciones.
- `Vehiculos.py`: Contiene las subclases `Aereo`, `Ferroviario`, `Automotor` y `Maritimo`, con sus atributos y lógica de cálculo según restricciones.
- `Solicitud.py`: Estructura las solicitudes de envío.
- `CargaNodos.py`, `CargaConexiones.py`, `CargaSolicitudes.py`: Módulos para leer los archivos CSV.
- `mostrar_mejores_caminos.py`: Muestra los itinerarios óptimos para cada solicitud.
- `graficos.py`: Genera gráficos requeridos para visualizar el progreso del viaje.

## Archivos de Entrada
Se utilizaron archivos `.csv`:
- `nodos.csv`: Lista de ciudades.
- `conexiones.csv`: Información de los tramos, distancias y restricciones.
- `solicitudes.csv`: Cargas a transportar, con origen, destino y peso.

## Lógica
1. Se filtran los caminos posibles entre origen y destino (evitando ciclos).
2. Se validan las restricciones según tipo de transporte.
3. Para cada itinerario válido, se calculan:
   - Tiempo total (según velocidad y distancias).
   - Costo total (según costo fijo, por km, y por kg).
4. Se eligen los caminos óptimos para cada KPI.

## Visualización Gráfica
El sistema genera los gráficos obligatorios:
- Distancia acumulada vs Tiempo acumulado
- Costo acumulado vs Distancia acumulada

## Decisiones de Diseño y Desafíos
- Se implementó la validación de restricciones directamente en el momento de buscar caminos, evitando caminos no viables desde el inicio.
- Las subclases de vehículos fueron diseñadas para sobrescribir métodos de cálculo de costo o tiempo según el modo (por ejemplo, el avión ajusta su velocidad por clima).
- Se diseñó la clase `RedTransporte` para encapsular toda la lógica del sistema, permitiendo escalar el modelo fácilmente a más nodos o solicitudes.
- Los datos se cargan desde CSV para facilitar pruebas con distintos escenarios.

## Resultados
El sistema lee correctamente los datos, genera los caminos óptimos para cada solicitud y muestra:
- El modo elegido
- La secuencia de ciudades
- El tiempo y el costo totales
- Gráficos correspondientes

Integrantes:
- Juan Cruz Gradin
- Juan Serra
- Lucas Firmenich
- Manuel Prieto Salazar
- Margarita Sottosanto
