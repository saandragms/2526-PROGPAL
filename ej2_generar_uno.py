import time
from random import randint, gauss
from multiprocessing import Pool
from itertools import starmap


def zeta(s: float, cant_terms: int) -> float:
    # La serie solo converge y su valor es real para s>1 real, pero nos
    # da igual, porque nosotros solo usamos una cantidad finita de términos.
    return sum([1 / (n ** s) for n in range(1, cant_terms + 1)])


def azar_costoso(coste: int) -> float:
    return zeta(gauss(0, 1), coste)

def textos(coste: int, cant_datos_azar: int) -> str:
    numeros = [azar_costoso(coste) for _ in range(cant_datos_azar)]
    num_strings = [f'{num}' for num in numeros]  # Convierte los números a strings.
    str_total = ' '.join(num_strings)  # Une los strings separados por blancos.
    return str_total
    


if __name__ == '__main__':
    cant_datos = 200_000
    cant_datos_azar = randint(cant_datos // 2, 2 * cant_datos)
    # Cada ejecución produce distinta cantidad de datos.
    coste = 1_000
    coste_azar = randint(coste // 2, 2 * coste)
    # En cada ejecución el coste es distinto.
    nombre_archivo = 'datos'

    t0 = time.perf_counter()

    numeros = [azar_costoso(coste_azar) for _ in range(cant_datos_azar)]
    num_strings = [f'{num}' for num in numeros]  # Convierte los números a strings.
    str_total = ' '.join(num_strings)  # Une los strings separados por blancos.
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(str_total)

    t1 = time.perf_counter()
    print(f'tiempo sin programacion paralela: {t1 - t0:.4f} segundos')
    
    sub_cant_datos = cant_datos_azar // 20
    tareas = [(coste_azar,sub_cant_datos)]*20 
    t0 = time.perf_counter()
    
    pool = Pool(4)
    str_totales = pool.starmap(textos,tareas)
    
    for i in range(len(str_totales)):
        nombre_archivo = f'datos{i}'
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(str_totales[i])
    t1 = time.perf_counter()
    print(f'tiempo con programación paralela: {t1 - t0:.4f} segundos')
    
    
    
