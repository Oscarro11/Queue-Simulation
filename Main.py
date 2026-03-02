import simpy
import numpy as np

import Processes

procesos_a_generar = 25
CPUs_disponibles = 1
velocidad_procesador = 3
velocidad_generacion_procesos = 10
seed = 44

procesador = Processes.Processor()
procesador.single_run(CPUs_disponibles, procesos_a_generar, velocidad_procesador, velocidad_generacion_procesos, seed)

print(round(procesador.metrics.get("mean_tiempo_en_sistema", 0.0)), 2)
print(round(procesador.metrics.get("std_tiempo_en_sistema", 0.0)), 2)