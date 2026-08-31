import streamlit as st
import numpy as np
import pandas as pd

# 1. BASE DE DATOS (En un proyecto final, esto se descarga de una API como nfl_data_py)
nfl_teams = {
    "Kansas City Chiefs": {"Off_Pts": 27.5, "Def_Pts": 19.2, "Std_Dev": 6.5},
    "Las Vegas Raiders": {"Off_Pts": 18.4, "Def_Pts": 24.5, "Std_Dev": 7.2},
    "Baltimore Ravens": {"Off_Pts": 28.4, "Def_Pts": 16.5, "Std_Dev": 6.1},
    "Miami Dolphins": {"Off_Pts": 29.2, "Def_Pts": 23.0, "Std_Dev": 8.5},
    "San Francisco 49ers": {"Off_Pts": 28.9, "Def_Pts": 17.5, "Std_Dev": 5.8}
}

# 2. CALENDARIO AUTOMÁTICO (Simulación de los encuentros de la semana)
partidos_semana = [
    "Kansas City Chiefs vs Miami Dolphins",
    "Baltimore Ravens vs Las Vegas Raiders",
    "San Francisco 49ers vs Kansas City Chiefs"
]

def predecir_partido_nfl(equipo_local, equipo_visitante, simulaciones=10000):
    exp_pts_local = (nfl_teams[equipo_local]["Off_Pts"] + nfl_teams[equipo_visitante]["Def_Pts"]) / 2 + 1.5
    exp_pts_visitante = (nfl_teams[equipo_visitante]["Off_Pts"] + nfl_teams[equipo_local]["Def_Pts"]) / 2
    
    std_local = nfl_teams[equipo_local]["Std_Dev"]
    std_visitante = nfl_teams[equipo_visitante]["Std_Dev"]

    sim_local = np.round(np.random.normal(exp_pts_local, std_local, simulaciones))
    sim_visitante = np.round(np.random.normal(exp_pts_visitante, std_visitante, simulaciones))

    prob_local = np.sum(sim_local > sim_visitante) / simulaciones
    prob_visitante = np.sum(sim_visitante > sim_local) / simulaciones
    over_under = np.median(sim_local + sim_visitante)
    
    return prob_local, prob_visitante, exp_pts_local, exp_pts_visitante, over_under

# 3. INTERFAZ GRÁFICA DE LA PÁGINA WEB
st.set_page_config(page_title="Predicciones NFL", page_icon="🏈")
st.title("🏈 Modelo Predictivo NFL")
st.write("Selecciona un encuentro de la jornada actual para correr 10,000 simulaciones de Monte Carlo.")

# Menú desplegable para seleccionar el partido
partido_seleccionado = st.selectbox("Encuentros de la Semana:", partidos_semana)

# Botón para ejecutar el modelo
if st.button("Generar Predicción"):
    # Extraemos los nombres de los equipos desde el texto del menú
    equipo_local, equipo_visitante = partido_seleccionado.split(" vs ")
    
    with st.spinner('Ejecutando 10,000 simulaciones...'):
        prob_loc, prob_vis, pts_loc, pts_vis, ou = predecir_partido_nfl(equipo_local, equipo_visitante)
        
        # Mostramos los resultados en columnas visuales
        col1, col2 = st.columns(2)
        
        col1.metric(label=f"Probabilidad {equipo_local} (Local)", value=f"{prob_loc * 100:.1f}%")
        col2.metric(label=f"Probabilidad {equipo_visitante} (Visitante)", value=f"{prob_vis * 100:.1f}%")
        
        st.divider()
        
        col3, col4 = st.columns(2)
        col3.metric(label="Línea Over/Under", value=f"{ou:.1f} pts")
        col4.metric(label="Marcador Esperado", value=f"{pts_loc:.0f} - {pts_vis:.0f}")
        