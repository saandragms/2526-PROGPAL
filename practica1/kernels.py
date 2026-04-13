from gpu_memory import GPUMemory
from sm_memory import SMMemory
from threading import Barrier
from multiprocessing.synchronize import Lock as LockType


def incr(core_id: int, gpu_mem: GPUMemory, sm_mem: SMMemory, lock : LockType, _ : Barrier) -> None:
    if core_id < sm_mem.tam_bloque:
        idx = sm_mem.ini_bloque + core_id
        gpu_mem.res[idx] = gpu_mem.dato1[idx] + 1

def sumar(core_id: int, gpu_mem: GPUMemory, sm_mem:SMMemory, lock : LockType, _ : Barrier) -> None:
    if core_id < sm_mem.tam_bloque:
        idx = sm_mem.ini_bloque + core_id
        gpu_mem.res[idx] = gpu_mem.dato1[idx] + gpu_mem.dato2[idx]


def difuminar(core_id: int, gpu_mem: GPUMemory, sm_mem : SMMemory, lock : LockType, _ : Barrier) -> None:
    if core_id < sm_mem.tam_bloque:
        idx = sm_mem.ini_bloque + core_id
        sm_mem.datos[core_id] = gpu_mem.dato1[idx]

        _.wait()
        if core_id < sm_mem.tam_bloque:
            numero = 0.0
            #CALCULOS
            for vecino in range(-2,3):
                v_local = core_id + vecino
                v_global = idx + vecino

                if (v_global < 0): 
                    # Caso  borde izquierdo
                    numero += gpu_mem.dato1[0]

                elif (v_global >= gpu_mem.tam_datos.value): 
                    # Caso borde derecho
                    numero += gpu_mem.dato1[gpu_mem.tam_datos.value - 1]

                elif (0 <= v_local < sm_mem.tam_bloque): 
                    # Caso vecino dentro del bloque actual
                    numero += sm_mem.datos[v_local]

                else: 
                    # Caso vecino en otro bloque
                    numero += gpu_mem.dato1[v_global]

            gpu_mem.res[idx] = numero / 5
   

def escalar(core_id: int, gpu_mem: GPUMemory, sm_mem:SMMemory, lock : LockType, _) -> None:
    if core_id < sm_mem.tam_bloque:
        idx = sm_mem.ini_bloque + core_id
        producto = gpu_mem.dato1[idx] * gpu_mem.dato2[idx]

        # Se usa un candado para que un único dato se sume a la memoria global cada vez.
        lock.acquire()
        try:
            gpu_mem.res[0] += producto
        finally:
            lock.release()




INCR = 1
SUMAR = 2
DIFUMINAR = 3
ESCALAR = 4

KERNELS = {
    INCR: incr,
    SUMAR: sumar,
    DIFUMINAR: difuminar,
    ESCALAR: escalar,
}
