import numpy as np
import simpy

class Process(object):
    def __init__(self, identificador:int, env:simpy.Environment, CPU:simpy.Resource, 
                 RAM:simpy.Container, instrucciones_procesamiento:int, rng_memoria:np.random.Generator,
                 results:dict, trace:bool = False) -> None:
        self.identificador = identificador
        self.env = env
        self.CPU = CPU
        self.RAM = RAM
        self.rng = rng_memoria
        self.instrucciones_procesamiento = instrucciones_procesamiento
        self.momento_creacion = env.now
        self.results = results
        self.TRACE = trace

        self.instrucciones = round(self.rng.random() * (10 - 1) + 1)
        self.memoria = 0

        self.trace(f"El proceso '{self.identificador}' se ha generado en: {env.now:.2f}")
        self.action = env.process(self.admitir())

    def trace(self, msg):
        if self.TRACE:
            print(msg)

    def admitir(self):
        memoria_necesaria = round(self.rng.random() * (10 - 1) + 1)
        if memoria_necesaria < self.RAM.level:
            self.memoria = memoria_necesaria
            self.RAM.get(memoria_necesaria)
            yield self.env.timeout(1)

            self.trace(f"El proceso '{self.identificador}' ha sido admitido en la cola de 'ready'. Tiempo: {self.env.now:.2f}")
            self.action = self.env.process(self.procesar())

        yield self.env.timeout(1)

    def procesar(self): 
        with self.CPU.request() as rq:
            self.trace(f"El proceso '{self.identificador}' ha sido admitido en la cola de 'running'. Tiempo: {self.env.now:.2f}")
            yield rq
            yield self.env.timeout(1)

            self.instrucciones -= self.instrucciones_procesamiento
            self.RAM.put(self.memoria)
            if self.instrucciones <= 0:
                self.trace(f"El proceso '{self.identificador}' ha terminado de procesarse. Tiempo: {self.env.now:.2f}")
                self.results["tiempo_en_sistema"].append(self.env.now - self.momento_creacion)
            else:
                if round(self.rng.random() * (2 - 1) + 1) == 1:
                    self.trace(f"El proceso '{self.identificador}' ha regresado a la cola de 'waiting'. Tiempo: {self.env.now:.2f}")
                    self.action = self.env.process(self.admitir())
                else:
                    self.trace(f"El proceso '{self.identificador}' ha regresado la cola de 'ready'. Tiempo: {self.env.now:.2f}")
                    self.action = self.env.process(self.procesar())

#Pendiente de revisar, quiero ver si puede separase en dos archivos
class Processor(object):
    results: dict[str, list] = {}
    metrics: dict[str, float] = {}
    TRACE = False

    def __init__(self, trace:bool = False) -> None:
        self.TRACE = trace

    def single_run(self, CPUs_disponibles:int, cantidad_procesos:int, velocidad_procesador:int, velocidad_generacion_procesos:int, rng_seed:int):
        self.results["tiempo_en_sistema"] = []
        
        env = simpy.Environment()
        rng = np.random.default_rng(rng_seed)
        RAM = simpy.Container(env, init=100, capacity=100)
        CPU = simpy.Resource(env, capacity=CPUs_disponibles)

        env.process(self.process_generator(env, rng, CPU, RAM, velocidad_procesador, velocidad_generacion_procesos, cantidad_procesos))
        env.run()

        self.metrics["mean_tiempo_en_sistema"] = float(np.mean(self.results["tiempo_en_sistema"]))
        self.metrics["std_tiempo_en_sistema"] = float(np.std(self.results["tiempo_en_sistema"]))

    def process_generator(self, env:simpy.Environment, rng:np.random.Generator, CPU:simpy.Resource, RAM:simpy.Container, velocidad_procesador:int, interval:float, max:int):
        for i in range(max):
            inter_arrival_time = rng.exponential(1.0 / interval)
            yield env.timeout(inter_arrival_time)
            Process(i+1, env, CPU, RAM, velocidad_procesador, rng, self.results, self.TRACE)