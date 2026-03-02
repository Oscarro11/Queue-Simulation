import simpy
import numpy as np

import Processes

def process_generator(env:simpy.Environment, interval:float, max:int):
    for i in range(max):
        inter_arrival_time = rng.exponential(1.0 / interval)
        yield env.timeout(inter_arrival_time)
        Processes.Process(i+1, env, CPU, RAM, velocidad_procesador, rng)

numero_procesos = 25
numero_CPUs = 1
velocidad_procesador = 3
velocidad_generacion_procesos = 10
seed = 44

env = simpy.Environment()
rng = np.random.default_rng(seed)
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=numero_CPUs)

env.process(process_generator(env, velocidad_generacion_procesos, numero_procesos))
env.run()