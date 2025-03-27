#Realizar una función que permita contar 
# la cantidad total de caracteres alfabéticos, dígitos o caracteres especiales en una cadena.

def contar_caracteres(cadena):
    a=0
    b=0
    c=0
    for i in cadena:
        if i.isalpha():
            a+=1
        elif i.isdigit():
            b+=1
        else:
            c+=1
    print('especiales ' + str(c) )
    print('num ' +str( b))
    print( 'letra ' +str(a))        
CADENA='@@IIIGG5666'
contar_caracteres(CADENA)
    