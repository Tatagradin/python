import matplotlib.pyplot as plt
def graficar_conexiones_por_tipo(stats):
    tipos = list(stats['conexiones_por_tipo'].keys())
    cantidades = list(stats['conexiones_por_tipo'].values())

    plt.figure(figsize=(8, 5))
    plt.bar(tipos, cantidades)
    plt.title('Conexiones por tipo de transporte')
    plt.xlabel('Tipo de transporte')
    plt.ylabel('Cantidad de conexiones')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
