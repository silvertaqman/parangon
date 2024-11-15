import streamlit as st
import copy
# Función para comprobar la extensión de un archivo cargado
def check_extension(uploaded_data):
    # Realiza una copia profunda de los datos cargados para no modificar los datos originales
    copied_data = copy.deepcopy(uploaded_data)
    
    # Comprueba si la extensión del archivo es .xlsx (Excel)
    if copied_data.name.endswith('xlsx'):
        pass  # Puede hacer algo con el archivo, pero el código no muestra qué hacer
        # st.markdown(f"##### :heavy_check_mark: _:green[{copied_data.name}]_ subido correctamente ")
    else:
        # Muestra un mensaje de error si el formato del archivo no es válido
        st.error("Formato de archivo no válido. Por favor, carga un archivo Excel.")
        st.stop()  # Detiene la ejecución de la aplicación Streamlit si se encuentra un archivo con formato incorrecto
