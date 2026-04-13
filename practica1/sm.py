from multiprocessing import Process, Queue
from nucleo import Nucleo
# otras importaciones
from sm_memory import SMMemory
from gpu_memory import GPUMemory
from threading import Barrier
from multiprocessing.synchronize import Lock


class SM(Process):
    def __init__(self, cant_nucleos_por_sm: int, mem_gpu: GPUMemory, tam_mem_sm: int, q_bloques: Queue, lock: Lock) -> None:
        super().__init__()
        self.cant_nucleos_por_sm = cant_nucleos_por_sm
        self.mem_gpu = mem_gpu
        self.tam_mem_sm = tam_mem_sm
        self.q_bloques = q_bloques # Una cola de tuplas: (ini_bloque, tam_bloque)
        self.lock = lock

    def run(self) -> None:
        mem_sm = SMMemory(self.tam_mem_sm)
        core_id = Queue() 
        
        # La SM divide el bloque entre los nucleos
        b = True
        while b:
            # Se toma uno de los bloques y se asigna a la SM local la información (tamaño del bloque e indice de comienzo respecto a la memoria global)
            elem = self.q_bloques.get()
            if elem is not None:
                mem_sm.ini_bloque = elem[0]
                mem_sm.tam_bloque = elem[1]

                # Elems_faltantes será o bien 5 (el numero de nucleos por SM) o menos, en caso de que el tamaño del bloque sea menor.
                elems_faltantes = min(self.cant_nucleos_por_sm, mem_sm.tam_bloque)
                barrera = Barrier(elems_faltantes)
                nucleos = [Nucleo(self.mem_gpu, mem_sm, core_id, self.lock, barrera) for _ in range(self.cant_nucleos_por_sm)]
                for n in nucleos:
                    n.start()
                
                # La SM divide el trabajo para enviarlos a los Núcleos mediante una cola.
                for i in range(elems_faltantes):
                    core_id.put(i)
                # Cargar la cola con Centinelas cuando hay menos de "5" elementos.
                for _ in range(self.cant_nucleos_por_sm - elems_faltantes):
                    core_id.put(None)

                for n in nucleos:
                    n.join()

            else:
                b = False


        
