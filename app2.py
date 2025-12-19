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
st.title("Dashboard Matrícula")


# ----------------------------
# Rutas de los archivos HTML
# ----------------------------
archivos_html = {
    "Área": "matricula_area.html",
    "Gestión": "matricula_gestion.html",
    "Nivel": "matricula_nivel.html",
    "Treemap TIPDATO": "treemap_tipdato.html",
    "Predicción": "matricula_prediccion.html",
    "Docentes": "matricula_docentes.html",
    "Matriculados": "matricula_matriculados.html",
    "Grafico Final": "grafico_matricula.html"
}

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
tab_dashboard, tab_prediccion, tab_docentes = st.tabs(["Matriculados", "Predicción", "Docentes"])

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
