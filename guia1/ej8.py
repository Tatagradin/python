lista=['hola mundo python es python genial']
palabra='python'
j=0
def ej7(lista,palabra):
    for i in range(len(lista)-1, -1, -1):  # Iterar de atrás hacia adelante
        if lista[i] == palabra:
            lista.pop(i)  # Eliminar sin afectar índices aún no visitados
            
    print(lista) 

ej7(lista,palabra) 
#xq [i] nos trae letras no palabras y la palabra nuca va ser igual a la letra