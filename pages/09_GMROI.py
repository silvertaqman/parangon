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

        # Obtener un DataFrame transformado utilizando la función get_transformed_dataframe 
        df_transformed = backend.get_transformed_dataframe(response)

        # Obtener las tasas de mantener el inventario (ICRs) desde la sesión
        ICRs = st.session_state["total_sub"].loc["Tasa de mantener el inventario (ICR)"]

        # Combinar el DataFrame transformado con las tasas de ICR 
        df_transformed = backend.merge_icrs_gmroi(df_transformed, ICRs)

        # Filtrar por categoría
        cat = st.selectbox('Ingresa la categoría que quieres filtrar', df_transformed["cat_producto"].unique())
        df_filtered = df_transformed[df_transformed["cat_producto"] == cat]

        # Filtrar por subcategoría
        subcat = st.selectbox('Ingresa la subcategoría que quieres filtrar', ["Todos"]+df_filtered["subcat_producto"].unique().tolist())
        # Si el usuario selecciona una subcategoría se filtra por esta misma
        if subcat != "Todos":
            df_filtered = df_filtered[df_filtered["subcat_producto"] == subcat]
        
        # Crear dos pestañas, "Tabla" y "Exportar", para la visualización de datos
        tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])

        # En la pestaña "Tabla", mostrar el DataFrame filtrado utilizando la función show_df_evai 
        with tab_1:
            # En la pestaña "Tabla", mostrar tres subpestañas para ver productos positivos, negativos y todos
            with tab_1:
                todos, positivos, negativos = st.tabs(["Todos 🔹", "Positivos ⭕", "Negativos ❌"])
                # En la subpestaña "Todos", mostrar el DataFrame de todos los productos 
                with todos:
                    # Ordena de mayor a menor en base al EVAI
                    df_filtered_sorted = df_filtered.sort_values(by=['GMROI'], ascending=False)
                    # Muestra el reporte de productos estilizado
                    backend.show_df_gmroi(df_filtered_sorted)
                    # Crear un gráfico de barras para mostrar el EVAI por subcategoría
                    backend.barchart_gmroi(df_filtered_sorted, subcat)

                # En la subpestaña "Positivos", mostrar el DataFrame de productos positivos
                with positivos:
                    # Filtra por los productos que tengan EVAI positivo
                    df_filtered_pos = df_filtered[df_filtered["GMROI"]>=0]
                    # Ordena de mayor a menor en base al EVAI
                    df_filtered_pos = df_filtered_pos.sort_values(by=['GMROI'], ascending=False)
                    # Muestra el reporte de productos estilizado
                    backend.show_df_gmroi(df_filtered_pos)
                    # Crear un gráfico de barras para mostrar el EVAI por subcategoría
                    backend.barchart_gmroi(df_filtered_pos, subcat)

                # En la subpestaña "Negativos", mostrar el DataFrame de productos negativos 
                with negativos:
                    # Filtra por los productos que tengan EVAI negativo
                    df_filtered_neg = df_filtered[df_filtered["GMROI"]<0]
                    # Ordena de menor a mayor en base al EVAI
                    df_filtered_neg = df_filtered_neg.sort_values(by=['GMROI'], ascending=True)
                    # Muestra el reporte de productos estilizado
                    
                    backend.show_df_gmroi(df_filtered_neg)
                    # Crear un gráfico de barras para mostrar el EVAI por subcategoría
                    backend.barchart_gmroi(df_filtered_neg, subcat)

        # En la pestaña "Exportar", descargar el DataFrame filtrado con el nombre "EVAI" 
        with tab_2:
            backend.download_dataframe(df_transformed, name="EVAI")

if __name__ == '__main__':
    main()