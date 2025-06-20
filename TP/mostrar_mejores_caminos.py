from graficos import mostrar_graficos_itinerario

#hacemos una funcion para por cada solicitud que muestre los mejores caminos posib

def mostrar_mejores_caminos(red_transporte, vehiculos):
    print("\n=== Mejores caminos para cada solicitud ===")
    for solicitud in red_transporte.solicitudes:
        print(f"\nSolicitud: {solicitud}")
        resultados = red_transporte.mejores_caminos_para_solicitud(solicitud, vehiculos)  
        #mas rápido (KPI 1: Minimizar el Tiempo Total de Entrega)
        mas_rapido = resultados.get('mas_rapido')
        if mas_rapido is not None:
            # Convertir minutos a formato horas:minutos:segundos
            tiempo_total_horas = mas_rapido['tiempo_total']
            horas = int(tiempo_total_horas) #extraigo la parte entera del tiempo en hs
            minutos = int((tiempo_total_horas - horas) * 60) #extraigo los minutos
            segundos = int(((tiempo_total_horas - horas) * 60 - minutos) * 60) #extraigo los segundos que sobraron
            
            print(f"\nKPI 1: Minimizar el Tiempo Total de Entrega")
            print(f"La solución más rápida es:")
            print(f"  • Modo: {mas_rapido['modo']}")
            print(f"  • Itinerario: {mas_rapido['itinerario']}")
            # print(f"  • Costo total: ${mas_rapido['costo_total']:,.0f}") Esto lo usabamos para testear pero no es necesario
            print(f"  • Tiempo total: {horas}:{minutos:02d}:{segundos:02d}")
            
            # Generar gráficos para el camino más rápido
            if 'tramos' in mas_rapido:
                print(f"\nGenerando gráficos para el camino más rápido...")
                mostrar_graficos_itinerario(mas_rapido['tramos'])
        else:
            print("No hay camino más rápido disponible.")
            
        print()  # Línea en blanco para separar
        
        #mas barato (KPI 2: Minimizar el Costo Total del Transporte)
        mas_barato = resultados.get('mas_barato')
        if mas_barato is not None:
            #Convertir minutos a formato horas:minutos:segundos
            tiempo_total_horas = mas_barato['tiempo_total']
            horas = int(tiempo_total_horas)
            minutos = int((tiempo_total_horas - horas) * 60)
            segundos = int(((tiempo_total_horas - horas) * 60 - minutos) * 60)
            
            print(f"KPI 2: Minimizar el Costo Total del Transporte")
            print(f"La solución más barata es:")
            print(f"  • Modo: {mas_barato['modo']}")
            print(f"  • Itinerario: {mas_barato['itinerario']}")
            print(f"  • Costo total: ${mas_barato['costo_total']:,.0f}")
            # print(f"  • Tiempo total: {horas}:{minutos:02d}:{segundos:02d}") Analogo al de arriba
            
            # Generar gráficos para el camino más barato
            if 'tramos' in mas_barato:
                print(f"\nGenerando gráficos para el camino más barato...")
                mostrar_graficos_itinerario(mas_barato['tramos'])
        else:
            print("No hay camino más barato disponible.")