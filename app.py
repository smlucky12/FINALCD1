

import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
import os
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegressionModel


# ----------------------------
# Inicializar SparkSession UNA SOLA VEZ
# ----------------------------


# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="Dashboard Matrícula", layout="wide")
import base64

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Aplicar fondo
set_background("20640609-school-education-seamless-background.jpg")

st.title("Dashboard Matrícula")


# ----------------------------
# Rutas de los archivos HTML
# ----------------------------
archivos_html = {
    "Área": "matricula_area.html",
    "Gestión": "matricula_gestion.html",
    "Nivel": "matricula_nivel.html",
    "Treemap TIPDATO": "treemap_tipdato.html",
    "Grafico Final": "grafico_matricula.html"
}

archivos_html.update({
    "Docentes Gestión": "grafico_docentes_gestion.html",
    "Area1": "grafico_area.html",
    "Nivel Educativo": "grafico_nivel_educativo_bonito.html",
    "Nivel Modalidad": "grafico_docentes_nivel_modalidad.html"
})

# ----------------------------
# Función para mostrar HTML
# ----------------------------
def mostrar_html(archivo, height=500, ancho_max=1000):
    path = Path(archivo)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        html_content_centered = f"""
        <div style="display: flex; justify-content: center; width: 100%;">
            <div style="width: {ancho_max}px;">
                {html_content}
            </div>
        </div>
        """
        components.html(html_content_centered, height=height)
    else:
        st.warning(f"Archivo {archivo} no encontrado.")

# ----------------------------
# Crear pestañas principales
# ----------------------------
tab_dashboard, tab_docentes = st.tabs(["Matriculados", "Docentes"])

# ----------------------------
# Pestaña Dashboard Matriculados
# ----------------------------
with tab_dashboard:
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        mostrar_html(archivos_html["Área"])
    with row1_col2:
        mostrar_html(archivos_html["Treemap TIPDATO"])
    with row2_col1:
        mostrar_html(archivos_html["Gestión"])
    with row2_col2:
        mostrar_html(archivos_html["Nivel"])

    # Gráfico final a ancho completo
    mostrar_html(archivos_html["Grafico Final"], height=2000, ancho_max=1200)


  
# ----------------------------
# Pestaña Docentes
# ----------------------------
with tab_docentes:
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        mostrar_html(archivos_html["Docentes Gestión"], height=600)
    with row1_col2:
        mostrar_html(archivos_html["Area1"], height=500)

    with row2_col1:
        mostrar_html(archivos_html["Nivel Educativo"], height=700)
    with row2_col2:
        mostrar_html(archivos_html["Nivel Modalidad"], height=700)







