import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Explorador de operación",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Carga los datos que utilizará la aplicación."""
    datos = pd.read_csv("datos_ejemplo.csv")
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])
    return datos


df = cargar_datos()


# ================================================================
# INTRODUCCIÓN
# ================================================================

st.title("Explorador de operación")

st.write("""
Esta aplicación permite analizar los casos registrados
en diferentes áreas y regiones.

Su objetivo es visualizar el comportamiento de los casos,
identificar las áreas con mayor actividad y facilitar
la interpretación de los resultados mediante indicadores,
gráficas y filtros interactivos.
""")

st.caption("Desarrollado por: Ricardo Villarreal Bazán")


# ================================================================
# FILTROS
# ================================================================

st.sidebar.header("Filtros")

# Filtro por área
areas_disponibles = sorted(df["Área"].dropna().unique())

areas_seleccionadas = st.sidebar.multiselect(
    "Área",
    options=areas_disponibles,
    default=areas_disponibles
)

# Filtro por región
regiones_disponibles = sorted(df["Región"].dropna().unique())

regiones_seleccionadas = st.sidebar.multiselect(
    "Región",
    options=regiones_disponibles,
    default=regiones_disponibles
)

# Aplicamos los filtros seleccionados
df_filtrado = df[
    (df["Área"].isin(areas_seleccionadas)) &
    (df["Región"].isin(regiones_seleccionadas))
].copy()


# ================================================================
# NAVEGACIÓN POR PESTAÑAS
# ================================================================

tab1, tab2 = st.tabs([
    "Resultados",
    "Metodología y limitaciones"
])


# ================================================================
# PESTAÑA 1: RESULTADOS
# ================================================================

with tab1:

    st.header("Resultados del análisis")

    # Indicadores principales
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Total de casos",
            value=int(df_filtrado["Casos"].sum())
        )

    with col2:
        st.metric(
            label="Registros analizados",
            value=len(df_filtrado)
        )

    if not df_filtrado.empty:

        # Gráfica de casos por fecha
        casos_por_fecha = (
            df_filtrado.groupby("Fecha", as_index=False)["Casos"]
            .sum()
            .sort_values("Fecha")
        )

        fig = px.line(
            casos_por_fecha,
            x="Fecha",
            y="Casos",
            markers=True,
            title="Casos por fecha"
        )

        st.plotly_chart(fig, width="stretch")

        # Gráfica de casos por área
        casos_por_area = (
            df_filtrado.groupby("Área", as_index=False)["Casos"]
            .sum()
            .sort_values("Casos", ascending=False)
        )

        fig_area = px.bar(
            casos_por_area,
            x="Área",
            y="Casos",
            title="Total de casos por área"
        )

        st.plotly_chart(fig_area, width="stretch")

        # Tabla de resultados
        st.subheader("Datos disponibles")

        st.dataframe(
            df_filtrado,
            width="stretch",
            hide_index=True
        )

        # CONCLUSIÓN AUTOMÁTICA
        st.subheader("Conclusión y recomendación")

        area_mayor = casos_por_area.iloc[0]["Área"]
        total_mayor = casos_por_area.iloc[0]["Casos"]

        st.success(
            f"El área con mayor número de casos es "
            f"{area_mayor}, con un total de {total_mayor} casos. "
            f"Se recomienda revisar esta área para comprender "
            f"las razones de su volumen de actividad."
        )

    else:
        st.warning(
            "No existen datos para los filtros seleccionados."
        )


# ================================================================
# PESTAÑA 2: METODOLOGÍA Y LIMITACIONES
# ================================================================

with tab2:

    st.header("Metodología")

    st.write("""
    Para realizar este análisis se utilizó el archivo
    datos_ejemplo.csv.

    Los datos se procesaron utilizando Pandas y se
    visualizaron mediante Plotly y Streamlit.

    Los resultados se calcularon agrupando los casos
    por fecha y por área.
    """)

    st.subheader("Fuentes")

    st.write("""
    Fuente de información: archivo datos_ejemplo.csv,
    proporcionado para la actividad.
    """)

    st.subheader("Limitaciones")

    st.write("""
    - Los resultados dependen de los registros disponibles.
    - Los filtros pueden modificar las conclusiones.
    - La cantidad de casos no explica por sí sola
      las causas de su comportamiento.
    - No se realizan predicciones futuras.
    """)
