import numpy as np
import simpy

class Process(object):
    def __init__(self, identificador:int, env:simpy.Environment, CPU:simpy.Resource, RAM:simpy.Container, instrucciones_procesamiento:int, rng_memoria:np.random.Generator) -> None:
        self.identificador = identificador
        self.env = env
        self.CPU = CPU
        self.RAM = RAM
        self.rng = rng_memoria
        self.instrucciones_procesamiento = instrucciones_procesamiento

        self.instrucciones = round(self.rng.random() * (10 - 1) + 1)
        self.memoria = 0

        print(f"El proceso '{self.identificador}' se ha generado en: {env.now:.2f}")
        self.action = env.process(self.admitir())

    def admitir(self):
        memoria_necesaria = round(self.rng.random() * (10 - 1) + 1)
        if memoria_necesaria < self.RAM.level:
            self.memoria = memoria_necesaria
            self.RAM.get(memoria_necesaria)
            yield self.env.timeout(1)

            print(f"El proceso '{self.identificador}' ha sido admitido en la cola de 'ready'. Tiempo: {self.env.now:.2f}")
            self.action = self.env.process(self.procesar())

        yield self.env.timeout(1)

    def procesar(self): 
        with self.CPU.request() as rq:
            print(f"El proceso '{self.identificador}' ha sido admitido en la cola de 'running'. Tiempo: {self.env.now:.2f}")
            yield rq
            yield self.env.timeout(1)

            self.instrucciones -= self.instrucciones_procesamiento
            self.RAM.put(self.memoria)
            if self.instrucciones <= 0:
                print(f"El proceso '{self.identificador}' ha terminado de procesarse. Tiempo: {self.env.now:.2f}")
            else:
                if round(self.rng.random() * (2 - 1) + 1) == 1:
                    print(f"El proceso '{self.identificador}' ha regresado a la cola de 'waiting'. Tiempo: {self.env.now:.2f}")
                    self.action = self.env.process(self.admitir())
                else:
                    print(f"El proceso '{self.identificador}' ha regresado la cola de 'ready'. Tiempo: {self.env.now:.2f}")
                    self.action = self.env.process(self.procesar())