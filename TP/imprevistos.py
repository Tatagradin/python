import random
pila_imprevistos=[]

probabilidades_paro = {
    "aerea": 0.3,
    "maritimo": 0.1,
    "ferroviaria": 0.15
}

probabilidades_corte = {
    "automotor": 0.25,
    "ferroviaria": 0.10
}

def conexion_esta_disponible(conexion, vehiculo):
    tipo = conexion.get_tipo_transporte().lower()
    ciudad1 = conexion.get_nombre_ciudad1()
    ciudad2 = conexion.get_nombre_ciudad2()

   #paro es LIFO
    if tipo in probabilidades_paro:
        if random.random() < probabilidades_paro[tipo]:
            mensaje = f"  Paro detectado en el sector {tipo.upper()} — Conexión entre {ciudad1} y {ciudad2} inhabilitada."
            pila_imprevistos.append(("paro", tipo, ciudad1, ciudad2, mensaje))
            #print(mensaje)
            return False
    #corte lifo
    if tipo in probabilidades_corte:
        if random.random() < probabilidades_corte[tipo]:
            mensaje = f"  Corte de ruta en transporte {tipo.upper()} — Conexión entre {ciudad1} y {ciudad2} inhabilitada."
            pila_imprevistos.append(("corte", tipo, ciudad1, ciudad2, mensaje))
            #print(mensaje)
            return False

  
    return conexion.es_valida_para_vehiculo(vehiculo)