import random

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
    tipo = conexion.tipo_transporte.lower()
    ciudad1 = conexion.get_nombre_ciudad1()
    ciudad2 = conexion.get_nombre_ciudad2()

   
    if tipo in probabilidades_paro:
        if random.random() < probabilidades_paro[tipo]:
            print(f"  Paro detectado en el sector {tipo.upper()} — Conexión entre {ciudad1} y {ciudad2} inhabilitada.")
            return False

    if tipo in probabilidades_corte:
        if random.random() < probabilidades_corte[tipo]:
            print(f"  Corte de ruta en transporte {tipo.upper()} — Conexión entre {ciudad1} y {ciudad2} inhabilitada.")
            return False

  
    return conexion.es_valida_para_vehiculo(vehiculo)