import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from Processes import Processor

if "active_dataframe" not in st.session_state:
    st.session_state["dataframes_resultados"] = []
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
    st.session_state["dataframes_resultados"].append(resultados)
    st.dataframe(st.session_state["active_dataframe"])

if st.button("Reiniciar datos"):
    st.session_state["dataframes_resultados"] = []
    st.session_state["dataframe_parametros"] = pd.DataFrame(columns=["Procesos a generar", "CPUs disponibles", "Cantidad de instrucciones", "Intervalo de generacion"])
    st.session_state["active_dataframe"] = pd.DataFrame()

variable = st.selectbox("Variable", st.session_state["active_dataframe"].columns)
metrica = st.selectbox("Metrica", st.session_state["active_dataframe"].index)
parametro_de_medida = st.selectbox("Parametro de medida", st.session_state["dataframe_parametros"].columns)

if st.button("Generar graficas"):
    resultados_generales = pd.DataFrame(columns=[f"{variable} / {metrica}"])

    for i in range(len(st.session_state["dataframes_resultados"])):
        resultados_generales.loc[st.session_state["dataframe_parametros"].loc[i][parametro_de_medida]] = (
            st.session_state["dataframes_resultados"][i].loc[metrica][variable])

    fig, ax = plt.subplots()

    resultados_generales.plot(ax=ax)

    ax.set_title("Comparacion de resultado vs experimento")
    ax.set_xlabel(parametro_de_medida)
    ax.set_ylabel(f"{variable} / {metrica}")

    st.pyplot(fig)