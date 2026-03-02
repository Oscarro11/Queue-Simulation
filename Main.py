import simpy
import numpy as np
import pandas as pd

import Processes

procesos_a_generar = 25
CPUs_disponibles = 1
velocidad_procesador = 3
velocidad_generacion_procesos = 10
seed = 44

procesador = Processes.Processor()
procesador.single_run(CPUs_disponibles, procesos_a_generar, velocidad_procesador, velocidad_generacion_procesos, seed)

mostrar_resultados = pd.DataFrame(procesador.results)
print(mostrar_resultados.describe() )