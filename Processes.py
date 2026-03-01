import random

class Process:
    instrucciones = -1
    estado = ""

    def __init__(self, instrucciones:int) -> None:
        self.instrucciones = instrucciones

class Processor:
    memoria_disponible = -1
    instrucciones_proceso = -1

    def __init__(self, memoria:int, instrucciones_proceso:int) -> None:
        self.memoria_disponible = memoria
        self.instrucciones_proceso = instrucciones_proceso

    def evaluar_nuevo(self, proceso:Process) -> bool:
        memoria_solicitada = random.randint(1, 10)
        if memoria_solicitada < self.memoria_disponible:
            self.memoria_disponible -= memoria_solicitada
            proceso.estado = "ready"
            return True
        
        else:
            proceso.estado = "waiting"
            return False
        
    def procesar_pendiente(self, proceso:Process) -> bool:
        proceso.instrucciones -= self.instrucciones_proceso
        if proceso.instrucciones <= 0:
            return True
        else:
            return False
        
    def evaluar_continuacion(self, proceso:Process) -> bool:
        if random.randint(1, 2) == 1:
            proceso.estado = "waiting"
            return False
        else:
            proceso.estado = "ready"
            return True