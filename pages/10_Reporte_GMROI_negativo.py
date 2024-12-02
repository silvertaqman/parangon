# Importar las bibliotecas necesarias
import streamlit as st
import database
from utils import backend


# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)

if not st.session_state.get("data_ready", False):
    st.error("Los datos no están disponibles. Completa el proceso de ingreso de datos para acceder a esta página.")
    st.stop()
def main():
    # Comprueba el estado de autenticación del usuario
    if st.session_state["authentication_status"] is False:
        # Muestra un mensaje de error si la autenticación es incorrecta
        st.error('Usuario/contraseña incorrecto')
    elif st.session_state["authentication_status"] is None:
        # Muestra un mensaje de advertencia si aún no se ha ingresado usuario y contraseña
        st.warning('Por favor ingresa tu usuario y contraseña')
    elif st.session_state["authentication_status"]:
        # Si la autenticación es exitosa, muestra el contenido principal.

        # Obtener la respuesta del servicio de base de datos utilizando el nombre de usuario almacenado en la sesión
        response = database.get_drive(st.session_state["username"])

        # Obtener un DataFrame transformado 
        df_transformed = backend.get_transformed_dataframe(response)

        # Obtener las tasas de mantener el inventario (ICRs) desde la sesión
        ICRs = st.session_state["total_sub"].loc["Tasa de mantener el inventario (ICR)"]

        # Muestra las gráficas de pie y EVAI vs productos dependiendo del df que se le ingrese
        def show_viz(df):
            # Crear dos columnas, una para el gráfico de barras y otra para el gráfico de pastel
            col1, col2 = st.columns([0.8, 0.2])

            # En la primera columna, mostrar el gráfico de barras para todos los productos utilizando barchart_all_products del módulo backend
            with col1:
                backend.barchart_all_products_gmroi(df)

            # En la segunda columna, mostrar el gráfico de pastel para todos los productos utilizando piechart_all_products del módulo backend
            with col2:
                backend.piechart_all_products_gmroi(df)

        # Crear dos pestañas, "Tabla" y "Exportar", para la visualización de datos
        tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])

        # En la pestaña "Tabla", mostrar tres subpestañas para ver productos positivos, negativos y todos
        with tab_1:
            todos, positivos, negativos = st.tabs(["Todos 🔹", "Positivos ⭕", "Negativos ❌"])
            
            # En la subpestaña "Todos", mostrar el DataFrame de todos los productos 
            with todos:
                df_all = backend.show_df_repgmroi(df_transformed, ICRs)
                show_viz(df_all)

            # En la subpestaña "Positivos", mostrar el DataFrame de productos positivos
            with positivos:
                df_positivos = backend.show_df_repgmroi(df_transformed, ICRs, range="positive")
                show_viz(df_positivos)

            # En la subpestaña "Negativos", mostrar el DataFrame de productos negativos 
            with negativos:
                df_negativos = backend.show_df_repgmroi(df_transformed, ICRs, range="negative")
                show_viz(df_negativos)

        # En la pestaña "Exportar", descargar el DataFrame de todos los productos con el nombre "reporte_EVAI_negativo" utilizando download_dataframe del módulo backend
        with tab_2:
            backend.download_dataframe(df_all, name="reporte_EVAI_negativo")

        

if __name__ == '__main__':
    main()