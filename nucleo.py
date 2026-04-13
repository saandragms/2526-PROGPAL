from threading import Thread, Barrier
# otras importaciones
from gpu_memory import GPUMemory
from sm_memory import SMMemory
from kernels import KERNELS
from multiprocessing import Queue
from multiprocessing.synchronize import Lock

class Nucleo(Thread):
    def __init__(self, gpu_mem: GPUMemory, sm_mem: SMMemory, q_ids: Queue, lock : Lock, barrera : Barrier) -> None:
        super().__init__()
        self.q_ids = q_ids
        self.gpu_mem = gpu_mem
        self.sm_mem = sm_mem
        self.lock = lock
        self.barrier = barrera

    def run(self) -> None:
        # Se toma índice del núcleo al que se va a enviar los datos.
        id = self.q_ids.get()
        if id is not None:
            # Se procesan los datos con el KERNEL seleccionado el gpu.py
            KERNELS[self.gpu_mem.kernel.value](id, self.gpu_mem, self.sm_mem, self.lock, self.barrier)


