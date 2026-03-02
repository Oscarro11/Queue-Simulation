import pandas as pd
import streamlit as stl

from Processes import Processor

stl.title("Simulacion de colas en CPU")
procesos_a_generar = stl.slider("Procesos a generar", 25, 300, 25, 25)
CPUs_disponibles = stl.slider("CPUs disponibles", 1, 8, 1, 1)
velocidad_procesador = stl.slider("Cantidad de instrucciones procesadas al mismo tiempo", 1, 8, 1, 1)
velocidad_generacion_procesos = stl.slider("Intervalo en generacion de procesos", 5, 300, 5, 5)
seed = 44

if stl.button("Realizar simulacion"):
    procesador = Processor()
    procesador.single_run(CPUs_disponibles, procesos_a_generar, velocidad_procesador, velocidad_generacion_procesos, seed)

    resultados = pd.DataFrame(procesador.results)
    stl.dataframe(resultados.describe())