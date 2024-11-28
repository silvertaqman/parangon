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
    #print(f"Configuración cargada: {env_settings}")
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

    # Verificar que el usuario esté configurado
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

    # Pestaña "Parámetros Inventario"
    with tab2:
        st.subheader("Datos de Inventario")
        collected_data["inventario"]["datos"] = recolectar_datos(inventario.datos, "inventario_datos")

        st.subheader("Costos y Gastos de Inventario")
        collected_data["inventario"]["costos_gastos"] = recolectar_datos(inventario.costos_gastos, "inventario_costos")

    # Pestaña "Parámetros Generales"
    with tab3:
        st.subheader("Financieros Generales")
        collected_data["generales"]["financieros"] = recolectar_datos(generales.financieros, "generales_financieros")

        st.subheader("Operativos Generales")
        collected_data["generales"]["operativos"] = recolectar_datos(generales.operativos, "generales_operativos")
        
    # Botón para guardar todos los datos
    if st.button("Enviar Todo"):
        success = True

        # Unir todos los datos recolectados en una sola estructura para la fila única
        combined_data = {}
        for category, sections in collected_data.items():
            record = {}
            for section_data in sections.values():
                record |= section_data
            combined_data[category] = record
            combined_data[category]["username"] = st.session_state["username"]
            try:
                final_model = Model(table_name=category)  # Cambiar por el nombre real de la tabla
                final_controller = Controller(final_model, View())

                # Validar y guardar los datos combinados
                if final_controller.validate_data(combined_data[category]):
                    message = final_controller.save_data(combined_data[category], db_config)
                    st.success(message)
                else:
                    st.error("Error al validar los datos.")
                    success = False
            except Exception as e:
                st.error(f"Error al procesar los datos: {e}")
                success = False

        if success:
            st.success("¡Proceso completado exitosamente!")
        else:
            st.error("Hubo errores al guardar los datos combinados. Revisa el log.")

if __name__ == '__main__':
    main()
