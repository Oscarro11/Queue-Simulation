import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from Processes import Processor

if "active_dataframe" not in st.session_state:
    st.session_state["dataframes_resultados"] = []
    st.session_state["dataframes_resultados_activo"] = []
    st.session_state["dataframe_parametros"] = pd.DataFrame(columns=["Procesos a generar", "CPUs disponibles", "Cantidad de instrucciones", "Intervalo de generacion"])
    st.session_state["active_dataframe"] = pd.DataFrame()

st.title("Simulacion de colas en CPU")
procesos_a_generar = st.slider("Procesos a generar", 25, 300, 25, 25)
CPUs_disponibles = st.slider("CPUs disponibles", 1, 8, 1, 1)
velocidad_procesador = st.slider("Cantidad de instrucciones procesadas al mismo tiempo", 1, 8, 1, 1)
velocidad_generacion_procesos = st.slider("Intervalo en generacion de procesos", 1, 20, 1, 1)
seed = 44

if st.button("Realizar simulacion"):
    procesador = Processor()
    procesador.single_run(CPUs_disponibles, procesos_a_generar, velocidad_procesador, velocidad_generacion_procesos, seed)

    st.session_state["dataframe_parametros"].loc[len(st.session_state["dataframe_parametros"])] = [procesos_a_generar, CPUs_disponibles, velocidad_procesador, velocidad_generacion_procesos]

    resultados = pd.DataFrame(procesador.results).describe()
    st.session_state["active_dataframe"] = resultados
    st.session_state["dataframes_resultados_activo"].append(resultados)
    st.dataframe(st.session_state["active_dataframe"])

if st.button("Grabar serie"):
    st.session_state["dataframes_resultados"].append(st.session_state["dataframes_resultados_activo"])
    st.session_state["dataframes_resultados_activo"] = []

if st.button("Reiniciar datos"):
    st.session_state["dataframes_resultados"] = []
    st.session_state["dataframes_resultados_activo"] = []
    st.session_state["dataframe_parametros"] = pd.DataFrame(columns=["Procesos a generar", "CPUs disponibles", "Cantidad de instrucciones", "Intervalo de generacion"])
    st.session_state["active_dataframe"] = pd.DataFrame()

variable = st.selectbox("Variable", st.session_state["active_dataframe"].columns)
metrica = st.selectbox("Metrica", st.session_state["active_dataframe"].index)
parametro_de_medida = st.selectbox("Parametro de medida", st.session_state["dataframe_parametros"].columns)

if st.button("Generar graficas"):
    fig, ax = plt.subplots()

    for dataframe_list in st.session_state["dataframes_resultados"]:
        resultados_generales = pd.DataFrame(columns=[f"{variable} / {metrica}", f"{parametro_de_medida}"])

        for i in range(len(dataframe_list)):
            dataframe = dataframe_list[i]
            resultados_generales.loc[i] = (dataframe.loc[metrica][variable], st.session_state["dataframe_parametros"].loc[i][parametro_de_medida])
        
        resultados_generales.plot.line(ax=ax, x=f"{parametro_de_medida}", y=f"{variable} / {metrica}")
        resultados_generales.plot.scatter(ax=ax, x=f"{parametro_de_medida}", y=f"{variable} / {metrica}", c="black")

    ax.set_title("Comparacion de resultado vs experimento")
    ax.set_xlabel(parametro_de_medida)
    ax.set_ylabel(f"{variable} / {metrica}")

    st.pyplot(fig)