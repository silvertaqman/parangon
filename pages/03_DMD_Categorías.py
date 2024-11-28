# Importar las bibliotecas necesarias
import streamlit as st
from utils import plot_df
from utils.do_df import download_dataframe
import data.db as db

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)

if "username" not in st.session_state or st.session_state["username"] is None:
    st.warning("No has iniciado sesión. Por favor, regresa a la página de inicio de sesión.")
    st.stop()


def main():
        # Título principal de la aplicación
        st.title("Data mining drivers por categoría")

        # Calcula una tabla de valores pivotantes por categoría de producto en base a la función del backend
        produc_table = plot_df.pivot_value_table(st.session_state["response"], 'cat_producto')
        # Calcula una tabla de porcentajes a partir de la tabla anterior
        percent_produc_table = plot_df.pivot_percent_table(produc_table)

        # Expansor para mostrar cálculo de drivers por categoría
        with st.expander("Cálculo de drivers por categoría"):
            # Crea dos pestañas para mostrar la tabla y permitir la exportación
            tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])
            with tab_1:
                # Muestra la tabla de valores pivotantes
                plot_df.show_pivot_value_table(produc_table)
            with tab_2:
                # Permite la descarga de la tabla en formato de archivo
                download_dataframe(produc_table, name="drivers_por_categoria")

        # Expansor para mostrar el porcentaje de drivers por categoría
        with st.expander("Porcentaje de drivers por categoría"):
            # Crea dos pestañas para mostrar la tabla y permitir la exportación
            tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])
            with tab_1:
                # Muestra la tabla de porcentajes
                plot_df.show_pivot_percent_table(percent_produc_table)
            with tab_2:
                # Permite la descarga de la tabla de porcentajes en formato de archivo
                download_dataframe(percent_produc_table, name="drivers_por_categoria_porcentaje")

        # Muestra un gráfico de barras basado en la tabla de porcentajes
        plot_df.show_barchart_dataminnigdrivers(percent_produc_table)

if __name__ == '__main__':
    main()
    