import time
from math import sqrt
from multiprocessing import Pool


def suma_sumacuadr_cant(nombre_de_archivo: str) -> tuple[int, int, int]:
    with open(nombre_de_archivo, 'r') as archivo:
        texto = archivo.read()  

    datos_str = texto.split()  
    datos = list(map(float, datos_str))  
    cant_datos = len(datos)  
    suma = sum(datos)  
    suma_cuadrados = sum([dato ** 2 for dato in datos]) 

    return (suma, suma_cuadrados, cant_datos)



if __name__ == '__main__':
    nombre_de_archivo = 'datos'
    
    t0 = time.perf_counter()
    
    with open(nombre_de_archivo, 'r') as archivo:
        texto = archivo.read()  # por ejemplo: texto = '1.0 2.0 3.0 4.0 5.0'
    datos_str = texto.split()  # datos_str = ['1.0', '2.0', '3.0', '4.0', '5.0']
    datos = list(map(float, datos_str))  # datos = [1.0, 2.0, 3.0, 4.0, 5.0]
    cant_datos = len(datos)  # cant_datos = 5
    suma = sum(datos)  # suma = 15.0
    suma_cuadrados = sum([dato ** 2 for dato in datos])  # suma_cuadrados = 55.0
    
    media = suma / cant_datos
    varianza = (suma_cuadrados / cant_datos) - (media ** 2)
    desviacion_tipica = sqrt(varianza)
    # aunque, en general, no sabemos si la distribución es normal
    
    t1 = time.perf_counter()
    
    print(f'media: {media:.4f}')
    print(f'desviación típica: {desviacion_tipica:.4f}')
    print(f'tiempo sin paralelo: {t1 - t0:.4f} segundos')

    t0 = time.perf_counter()

    pool = Pool(4)
    nombre_de_archivos = [f'datos{i}' for i in range(20)]

    tuplas = pool.map(suma_sumacuadr_cant,nombre_de_archivos)
    cant = sum([t[2] for t in tuplas])
    media_total = sum([t[0] for t in tuplas]) / cant
    varianza_total = (sum([t[1] for t in tuplas]) / cant) - (media_total ** 2)
    desviacion_tipica_total = sqrt(varianza_total)

    t1 = time.perf_counter()

    print(f'media: {media_total:.4f}')
    print(f'desviación típica: {desviacion_tipica_total:.4f}')
    print(f'tiempo con paralelo: {t1 - t0:.4f} segundos')
