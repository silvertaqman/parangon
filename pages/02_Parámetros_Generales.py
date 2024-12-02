import streamlit as st
from config.confloader import load_config, get_db_config
from utils.iosql_df import Almacenaje, Inventario, Generales, Model, View, Controller
import logging

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",
    page_icon="🏗️",
    layout="wide"
)

try:
    env_settings = load_config()
    db_config = get_db_config(env_settings)
except Exception as e:
    logging.error(f"Error al cargar la configuración: {e}")
    raise

def main():
    """
    Función principal para la carga y gestión de parámetros con objetos.
    """
    st.title('Ingresar parámetros de cada proceso')

    if "username" not in st.session_state:
        st.error("Inicia sesión para continuar")

    if not st.session_state["username"]:
        st.warning("Por favor, inicia sesión antes de continuar.")
        return

    # Crear instancias de las clases
    almacenaje = Almacenaje()
    inventario = Inventario()
    generales = Generales()

    # Diccionario para almacenar datos recolectados de cada pestaña
    collected_data = {"almacenaje": {}, "inventario": {}, "generales": {}}

    # Función para recolectar datos de una pestaña
    def recolectar_datos(columns, section_key):
        data = {}
        for key, label in columns.items():
            data[key] = st.text_input(f"{label}:", key=f"{section_key}_{key}")  # Inputs únicos
        return data

    # Función para manejar el envío de datos de una categoría
    def enviar_datos(categoria, datos_categoria):
        try:
            record = {}
            for section_data in datos_categoria.values():
                record |= section_data
            record["username"] = st.session_state["username"]

            final_model = Model(table_name=categoria)
            final_controller = Controller(final_model, View())

            if final_controller.validate_data(record):
                message = final_controller.save_data(record, db_config)
                st.success(f"Categoría '{categoria}' guardada: {message}")
            else:
                st.error(f"Error al validar los datos para '{categoria}'.")
        except Exception as e:
            st.error(f"Error procesando '{categoria}': {e}")

    # Crear pestañas para diferentes categorías
    tab1, tab2, tab3 = st.tabs(["Almacenaje", "Inventario", "Generales"])

    # Pestaña "Parámetros Almacenaje"
    with tab1:
        st.subheader("Datos de Almacenaje")
        collected_data["almacenaje"]["datos"] = recolectar_datos(almacenaje.datos, "almacenaje_datos")

        st.subheader("Costos y Gastos de Almacenaje")
        collected_data["almacenaje"]["costos_gastos"] = recolectar_datos(almacenaje.costos_gastos, "almacenaje_costos")

        st.subheader("Inversiones de Almacenaje")
        collected_data["almacenaje"]["inversiones"] = recolectar_datos(almacenaje.inversiones, "almacenaje_inversiones")

        if st.button("Enviar Almacenaje"):
            enviar_datos("almacenaje", collected_data["almacenaje"])

    # Pestaña "Parámetros Inventario"
    with tab2:
        st.subheader("Datos de Inventario")
        collected_data["inventario"]["datos"] = recolectar_datos(inventario.datos, "inventario_datos")

        st.subheader("Costos y Gastos de Inventario")
        collected_data["inventario"]["costos_gastos"] = recolectar_datos(inventario.costos_gastos, "inventario_costos")

        if st.button("Enviar Inventario"):
            enviar_datos("inventario", collected_data["inventario"])

    # Pestaña "Parámetros Generales"
    with tab3:
        st.subheader("Financieros Generales")
        collected_data["generales"]["financieros"] = recolectar_datos(generales.financieros, "generales_financieros")

        st.subheader("Operativos Generales")
        collected_data["generales"]["operativos"] = recolectar_datos(generales.operativos, "generales_operativos")

        if st.button("Enviar Generales"):
            enviar_datos("generales", collected_data["generales"])

if __name__ == '__main__':
    main()
