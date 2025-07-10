from graficos import Graficador
from Vehiculos import Aereo, Ferroviario, Maritimo, Automotor
class MostradorCaminos:
    def __init__(self):
        self.vehiculos = {
            'aereo': Aereo(),
            'maritimo': Maritimo(),
            'ferroviario': Ferroviario(),
            'automotor': Automotor()
        }

    def mostrar_mejores_caminos(self, red_transporte):
        print("\n=== Mejores caminos para cada solicitud ===")
        for solicitud in red_transporte.get_solicitud():
            print(f"\nSolicitud: {solicitud}")
            resultados = red_transporte.mejores_caminos_para_solicitud(solicitud, self.vehiculos)
            mas_rapido = resultados.get('mas_rapido')
            mas_barato = resultados.get('mas_barato')
            self.mostrar_camino_rapido(solicitud, mas_rapido)
            print()
            self.mostrar_camino_barato(solicitud, mas_barato)

    def mostrar_camino_rapido(self, solicitud, mas_rapido):
        if mas_rapido is not None:
            tiempo_total_horas = mas_rapido['tiempo_total']
            horas = int(tiempo_total_horas)
            minutos = int((tiempo_total_horas - horas) * 60)
            segundos = int(((tiempo_total_horas - horas) * 60 - minutos) * 60)
            print(f"\nKPI 1: Minimizar el Tiempo Total de Entrega")
            print(f"La solución más rápida es:")
            print(f"  • Modo: {mas_rapido['modo']}")
            print(f"  • Itinerario: {mas_rapido['itinerario']}")
            print(f"  • Tiempo total: {horas}:{minutos:02d}:{segundos:02d}")
            self.mostrar_grafico_si_corresponde(mas_rapido.get('tramos'), "camino más rápido")
        else:
            print("No hay camino más rápido disponible.")

    def mostrar_camino_barato(self, solicitud, mas_barato):
        if mas_barato is not None:
            tiempo_total_horas = mas_barato['tiempo_total']
            horas = int(tiempo_total_horas)
            minutos = int((tiempo_total_horas - horas) * 60)
            segundos = int(((tiempo_total_horas - horas) * 60 - minutos) * 60)
            print(f"KPI 2: Minimizar el Costo Total del Transporte")
            print(f"La solución más barata es:")
            print(f"  • Modo: {mas_barato['modo']}")
            print(f"  • Itinerario: {mas_barato['itinerario']}")
            print(f"  • Costo total: ${mas_barato['costo_total']:,.0f}")
            self.mostrar_grafico_si_corresponde(mas_barato.get('tramos'), "camino más barato")
        else:
            print("No hay camino más barato disponible.")

    def mostrar_grafico_si_corresponde(self, tramos, descripcion):
        if tramos:
            print(f"\nGenerando gráficos para el {descripcion}...")
            Graficador.mostrar_graficos_itinerario(tramos)
