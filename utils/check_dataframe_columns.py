import streamlit as st
import pandas as pd
import copy
import json
# Función para verificar si un DataFrame contiene las columnas esperadas
def check_dataframe_columns(uploaded_data):
    # Realiza una copia profunda de los datos cargados para no modificar los datos originales
    copied_data = copy.deepcopy(uploaded_data)
    
    # Lee el archivo Excel y carga su contenido en un DataFrame
    df = pd.read_excel(copied_data)
    
    # Obtiene la lista de nombres de columnas del DataFrame
    df_columns = df.columns.tolist()

    # ruta del JSON que contiene las columnas esperadas
    json_filename = 'json_files/database_names.json'
    
    # Abre y carga el contenido del archivo JSON en un diccionario
    with open(json_filename, 'r') as json_file:
        data_dictionary = json.load(json_file)
    
    # Obtiene la lista de columnas esperadas del diccionario cargado
    expected_columns = data_dictionary['expected_columns']

    # Encuentra las columnas que faltan en el DataFrame comparando con las columnas esperadas
    missing_columns = set(expected_columns) - set(df_columns)

    # Encuentra las columnas adicionales que no se esperaban en el DataFrame
    extra_columns = set(df_columns) - set(expected_columns)

    # Verifica si el DataFrame contiene exactamente las mismas columnas que se esperaban
    if len(missing_columns) == 0 and len(extra_columns) == 0:
        pass  # si cumple con las columnas se sigue con la ejecución normal
    else:
        # Muestra un mensaje de error si el DataFrame no contiene las mismas columnas que se esperaban
        st.error("El DataFrame no contiene exactamente las mismas columnas.")

        # Comprueba si hay columnas faltantes o columnas adicionales y muestra un mensaje de advertencia
        if len(missing_columns) > 0 or len(extra_columns) > 0:
            warning_message = ""  # Inicializa una cadena de advertencia vacía

            if len(missing_columns) > 0:
                # Si hay columnas faltantes, agrega un mensaje indicando cuáles son
                warning_message += f"Columnas faltantes: \n\n{list(missing_columns)}\n\n"

            if len(extra_columns) > 0:
                # Si hay columnas adicionales, agrega un mensaje indicando cuáles son
                warning_message += f"Columnas adicionales: \n\n{list(extra_columns)}"

            # Muestra una advertencia en la aplicación Streamlit con el mensaje construido
            st.warning(warning_message)

            # Detiene la ejecución de la aplicación Streamlit si las columnas no coinciden
            st.stop()
