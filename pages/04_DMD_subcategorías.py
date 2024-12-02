# Importar las bibliotecas necesarias
import streamlit as st
from utils.plot_df import *
from utils.do_df import download_dataframe

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)

#if not st.session_state.get("response", False):
#    st.error("Los datos no están disponibles. Completa el proceso de ingreso de datos para acceder a esta página.")
#    st.stop()

def main():
    # Comprueba el estado de autenticación del usuario
    if st.session_state["authentication_status"] is False:
        # Muestra un mensaje de error si la autenticación es incorrecta
        st.error('Usuario/contraseña incorrecto')
    elif st.session_state["authentication_status"] is None:
        # Muestra un mensaje de advertencia si aún no se ha ingresado usuario y contraseña
        st.warning('Por favor ingresa tu usuario y contraseña')
    elif st.session_state["authentication_status"]:
        # Si la autenticación es exitosa, muestra el contenido principal
        
        # Título principal de la aplicación 
        st.title("Data mining drivers por subcategoría")
    
        # Transforma los datos de la base de datos utilizando funciones del módulo "backend"
        saved_database = st.session_state["response"]

        # Calcula una tabla de valores pivotantes por categoría de producto en base a la función del backend
        produc_table = pivot_value_table(saved_database, "subcat_producto")

        # Calcula una tabla de porcentajes a partir de la tabla anterior
        percent_produc_table = pivot_percent_table(produc_table)

        # Expansor para mostrar cálculo de drivers por categoría
        with st.expander("Cálculo de drivers por categoría"):
            # Crea dos pestañas para mostrar la tabla y permitir la exportación
            tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])
            with tab_1:
                # Muestra la tabla de valores pivotantes
                show_pivot_value_table(produc_table)
            with tab_2:
                # Permite la descarga de la tabla en formato de archivo
                download_dataframe(produc_table, name="drivers_por_categoria")

        # Expansor para mostrar el porcentaje de drivers por categoría
        with st.expander("Porcentaje de drivers por categoría"):
            # Crea dos pestañas para mostrar la tabla y permitir la exportación
            tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])
            with tab_1:
                # Muestra la tabla de porcentajes
                show_pivot_percent_table(percent_produc_table)
            with tab_2:
                # Permite la descarga de la tabla de porcentajes en formato de archivo
                download_dataframe(percent_produc_table, name="drivers_por_categoria_porcentaje") 

        # Muestra un gráfico de barras basado en la tabla de porcentajes
        show_barchart_dataminnigdrivers(percent_produc_table)
        
if __name__ == '__main__':
    main()
        