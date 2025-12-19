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

with tab_prediccion:
    st.subheader("Predicción de Matrícula")
    st.info("Ingrese los valores para D01 a D12. Los demás datos se asignan automáticamente según la tabla interna.")

    # ----------------------------
    # Definir columnas: izquierda formulario, derecha resultado
    # ----------------------------
    col_formulario, col_resultado = st.columns([1, 1])

    # ----------------------------
    # Columna formulario
    # ----------------------------
    with col_formulario:
        valores = {}
        for i in range(1, 13):
            valores[f"D{i:02d}"] = st.number_input(f"D{i:02d}", min_value=0, value=0)  # valor inicial 0

        # Tabla interna para asignar Descripción, Sexo y Grado
        tabla = {
            "D01": {"Descripción": "Matrícula en 1° grado", "Sexo": "Hombre", "Grado": "1° grado"},
            "D02": {"Descripción": "Matrícula en 1° grado", "Sexo": "Mujer", "Grado": "1° grado"},
            "D03": {"Descripción": "Matrícula en 2° grado", "Sexo": "Hombre", "Grado": "2° grado"},
            "D04": {"Descripción": "Matrícula en 2° grado", "Sexo": "Mujer", "Grado": "2° grado"},
            "D05": {"Descripción": "Matrícula en 3° grado", "Sexo": "Hombre", "Grado": "3° grado"},
            "D06": {"Descripción": "Matrícula en 3° grado", "Sexo": "Mujer", "Grado": "3° grado"},
            "D07": {"Descripción": "Matrícula en 4° grado", "Sexo": "Hombre", "Grado": "4° grado"},
            "D08": {"Descripción": "Matrícula en 4° grado", "Sexo": "Mujer", "Grado": "4° grado"},
            "D09": {"Descripción": "Matrícula en 5° grado", "Sexo": "Hombre", "Grado": "5° grado"},
            "D10": {"Descripción": "Matrícula en 5° grado", "Sexo": "Mujer", "Grado": "5° grado"},
            "D11": {"Descripción": "Matrícula en 6° grado", "Sexo": "Hombre", "Grado": "6° grado"},
            "D12": {"Descripción": "Matrícula en 6° grado", "Sexo": "Mujer", "Grado": "6° grado"},
        }

        # ----------------------------
        # Botón para predecir
        # ----------------------------
        if st.button("Predecir"):
            try:
                from pyspark.sql import SparkSession
                from pyspark.ml.classification import LogisticRegressionModel

                # Inicializar Spark
                from pyspark.sql import SparkSession
                spark = SparkSession.builder \
                .config("spark.driver.memory", "4g") \
                .config("spark.executor.memory", "4g") \
                .getOrCreate()

                # Cargar modelo
                modelo_path = "modelo_logistico_spark"
                modelo = LogisticRegressionModel.load(modelo_path)

                # Crear DataFrame para todas las filas D01-D12
                lista_pred = []
                for d in valores:
                    fila = {**{"Descripción": tabla[d]["Descripción"],
                              "Sexo": tabla[d]["Sexo"],
                              "Grado": tabla[d]["Grado"]},
                            **{d: valores[d]}}
                    # Para las demás D no usadas, asignar None
                    for j in range(1, 13):
                        col = f"D{j:02d}"
                        if col not in fila:
                            fila[col] = None
                    lista_pred.append(fila)

                df_pred = spark.createDataFrame(lista_pred)

                # Hacer predicción
                predicciones = modelo.transform(df_pred)

                # Guardar resultado en session_state
                st.session_state['resultado'] = predicciones.toPandas()
            except Exception as e:
                st.error(f"Error al predecir: {e}")

    # ----------------------------
    # Columna resultado
    # ----------------------------
    with col_resultado:
        st.subheader("Resultado de la Predicción")
        if 'resultado' in st.session_state:
            st.dataframe(st.session_state['resultado'])
        else:
            st.info("Ingrese los datos y haga clic en Predecir para ver el resultado.")

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


