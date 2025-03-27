lista=['hola', 'mundo', 'python', 'es','python', 'genial']
palabra='python'
j=0
def ej7(lista,palabra):
    for i in range(len(lista)-1, -1, -1):  # Iterar de atrás hacia adelante
        if lista[i] == palabra:
            lista.pop(i)  # Eliminar sin afectar índices aún no visitados
            
    print(lista) 

ej7(lista,palabra)          

#Una forma de solucionar esto es iterar de atrás hacia adelante para 
# evitar que los índices cambien al eliminar elementos. 
# Alternativamente, podrías evitar modificar la lista mientras iteras, o ajustar el índice manualmente.