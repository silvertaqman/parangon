# Importar las bibliotecas necesarias
import streamlit as st
from utils.do_df import get_styled_dataframe, download_dataframe
import data.db as db
from config.confloader import load_config, get_db_config
import logging
import pandas as pd
from utils.structure_df import TransformDF

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)

# Cargar toda la configuración
try:
    env_settings = load_config()
    #print(f"Configuración cargada: {env_settings}")
except Exception as e:
    logging.error(f"Error al cargar la configuración: {e}")
    raise

# Obtener la configuración específica de PostgreSQL
db_config = get_db_config(env_settings)

def main():
    # Título de la página
    st.title("Base de datos :card_file_box:")
    st.write("Sube un archivo Excel para procesarlo y cargarlo a la base de datos.")

    # Variables iniciales en la sesión
    if "response" not in st.session_state:
        st.session_state["response"] = None

    # Cargar archivo
    uploaded_data = st.file_uploader(label="", label_visibility='collapsed', type=["xlsx", "xls"])
    
    if uploaded_data:
        try:
            # Leer archivo y transformarlo
            df = pd.read_excel(uploaded_data) if uploaded_data.name.endswith("xlsx") else pd.read_csv(uploaded_data)
            transform = TransformDF()  # Asegúrate de tener esta clase definida correctamente
            transform.check_df_columns(df)
            response = transform.calculate_df(df)
            st.session_state["response"] = response

            st.success("Archivo cargado y procesado correctamente.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            return

    # Si no hay archivo cargado, mostrar mensaje informativo
    if st.session_state["response"] is None:
        st.info("Por favor, carga un archivo Excel utilizando el botón de arriba.")
        return

    # Botón para subir a la base de datos
    if st.button("Subir a la base de datos"):
        try:
            transform = TransformDF()
            transform.to_db(st.session_state["response"], db_config) 
            st.toast("Archivo subido a la base de datos correctamente.", icon="✔️")
        except Exception as e:
            st.error(f"Error al subir el archivo a la base de datos: {e}")

    # Pestañas para mostrar y exportar
    tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])
    with tab_1:
        df_styled = get_styled_dataframe(st.session_state["response"])
        st.dataframe(df_styled, hide_index=True)
    with tab_2:
        # Exportar datos en CSV o Excel
        if st.session_state["response"] is not None:
            download_dataframe(st.session_state["response"], name="base_de_datos")

if __name__ == '__main__':
    main()


