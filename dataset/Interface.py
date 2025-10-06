# STREAMLIT interfaces graficas python
# usuario interactue con los resultados
# aplicacion sencilla introductoria

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px

# Desplegamos textos.
st.title("Product_Dev_Plan_vrs_Forecast")
st.subheader("Modelación y Simulación.")

# Leer el CSV
df = pd.read_csv("forecast_underperform.csv")

# Función para colorear filas en base a la columna "Ventas"
def highlight_row(row):
    if row["under_real"] == True:
        return ['background-color: #166124'] * len(row)  # Fila en verde
    elif row["under_real"] == False:
        return ['background-color: #EB9E94'] * len(row)  # Fila en rojo
    else:
        return [''] * len(row)  # Sin color

# Aplicar estilos
styled_df = df.style.apply(highlight_row, axis=1)

# Mostrar en Streamlit
st.dataframe(styled_df)

#------------------------------------
st.subheader("Seleccionar fila por número de índice")

# Suponiendo que el dataset ya está cargado en df
fila_seleccionada = st.number_input(
    "Ingrese el número de fila (índice) que desea ver:",
    min_value=0,
    max_value=len(df)-1,
    step=1
)

# Mostrar la fila seleccionada
st.subheader(f"Datos de la fila {fila_seleccionada}")
st.write(df.iloc[fila_seleccionada])

#------------------------------------------------------
# grafica interactiva zoom in/out 
# granualidad: cuanto aporta un producto especifico o restaurante o una combinacion
# plotlyb

# colorear filas verde arriba del plan, rojo abajo del plan
# revisar publicacion en repositorio de streamlit

#-------------------------------------------------------
# grafica
data = pd.read_csv("historical_forecast_sales.csv")
data['date'] = pd.to_datetime(data['date'])

# --- Simular plan financiero ---
mean = data['item_cnt_day'].fillna(data['forecast_item_cnt']).values
std = np.maximum(mean * 0.2, 1)
np.random.seed(42)
ventas_plan = np.random.normal(mean, std)
ventas_plan = np.clip(ventas_plan, 0, None)
data['ventas_plan'] = ventas_plan

# --- Transformar a formato largo para Plotly ---
data_long = data.melt(
    id_vars=['date'],
    value_vars=['item_cnt_day', 'forecast_item_cnt', 'ventas_plan'],
    var_name='Serie',
    value_name='Cantidad'
)

# --- Gráfico interactivo ---
fig = px.line(
    data_long,
    x='date',
    y='Cantidad',
    color='Serie',
    title="Ventas reales, forecast SARIMA y plan financiero simulado",
    markers=True
)

fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Cantidad de productos vendidos",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
