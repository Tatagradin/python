import matplotlib.pyplot as plt

def graficar_distancia_tiempo(tramos):

    tiempo_acum = [0]  # Iniciamos en 0
    distancia_acum = [0]  # Iniciamos en 0
    etiquetas = []
    
    # Acumulamos valores para cada tramo
    for tramo in tramos:
        tiempo_acum.append(tiempo_acum[-1] + tramo['tiempo'])
        distancia_acum.append(distancia_acum[-1] + tramo['distancia'])
        etiquetas.append(f"{tramo['origen']} ➜ {tramo['destino']}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo_acum, distancia_acum, marker='o', linestyle='-', color='blue')
    
    # Agregamos etiquetas para cada punto (excepto el origen)
    for i in range(len(etiquetas)):
        plt.annotate(etiquetas[i], 
                    (tiempo_acum[i+1], distancia_acum[i+1]),
                    xytext=(10, 10), textcoords='offset points')
    
    plt.title('Progreso del Itinerario: Distancia vs. Tiempo')
    plt.xlabel('Tiempo Acumulado (minutos)')
    plt.ylabel('Distancia Acumulada (km)')
    plt.grid(True)
    plt.tight_layout()
    
def graficar_costo_distancia(tramos):

    distancia_acum = [0]  # Iniciamos en 0
    costo_acum = [0]  # Iniciamos en 0
    etiquetas = []
    
    # Acumulamos valores para cada tramo
    for tramo in tramos:
        distancia_acum.append(distancia_acum[-1] + tramo['distancia'])
        costo_acum.append(costo_acum[-1] + tramo['costo'])
        etiquetas.append(f"{tramo['origen']} ➜ {tramo['destino']}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(distancia_acum, costo_acum, marker='s', linestyle='-', color='orange')
    
    # Agregamos etiquetas para cada punto (excepto el origen)
    for i in range(len(etiquetas)):
        plt.annotate(etiquetas[i], 
                    (distancia_acum[i+1], costo_acum[i+1]),
                    xytext=(10, 10), textcoords='offset points')
    
    plt.title('Progreso del Itinerario: Costo vs. Distancia')
    plt.xlabel('Distancia Acumulada (km)')
    plt.ylabel('Costo Acumulado ($ARS)')
    plt.grid(True)
    plt.tight_layout()

def mostrar_graficos_itinerario(tramos):

    graficar_distancia_tiempo(tramos)
    graficar_costo_distancia(tramos)
    plt.show()  # Muestra ambos gráficos

# Ejemplo de uso:
if __name__ == "__main__":
    # Datos de ejemplo
    tramos_ejemplo = [
        {'origen': 'Zárate', 'destino': 'Buenos Aires', 'distancia': 85, 'tiempo': 51, 'costo': 1365},
        {'origen': 'Buenos Aires', 'destino': 'Mar del Plata', 'distancia': 384, 'tiempo': 288, 'costo': 5850}
    ]
    
    mostrar_graficos_itinerario(tramos_ejemplo)
