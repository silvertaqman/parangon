import streamlit as st
from utils.structure_df import Almacenaje, Inventario, Generales
import data.db as db
from utils.iosql_df import create_table_charge_and_save

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",
    page_icon="🏗️",
    layout="wide"
)

def main():
    """
    Función principal para la carga y gestión de parámetros con objetos.
    """
    st.title('Ingresar parámetros por proceso')
    # Crear instancias de las clases
    almacenaje = Almacenaje()
    inventario = Inventario()
    generales = Generales()

    # Crear pestañas para diferentes categorías
    tab1, tab2, tab3 = st.tabs(["Almacenaje", "Inventario", "Generales"])

    # Pestaña "Parámetros Almacenaje"
    with tab1:
        create_table_charge_and_save(almacenaje, "datos", "Datos Almacenaje")
        st.divider()
        create_table_charge_and_save(almacenaje, "costos_gastos", "Costos y Gastos Almacenaje")
        st.divider()
        create_table_charge_and_save(almacenaje, "inversiones", "Inversiones Almacenaje")

    # Pestaña "Parámetros Inventario"
    with tab2:
        create_table_charge_and_save(inventario, "datos", "Datos Inventario")
        st.divider()
        create_table_charge_and_save(inventario, "costos_gastos", "Costos y Gastos Inventario")
        st.divider()
        create_table_charge_and_save(inventario, "inversiones", "Inversiones Inventario")

    # Pestaña "Parámetros Generales"
    with tab3:
        create_table_charge_and_save(generales, "financieros", "Datos Financieros", format="%")
        st.divider()
        create_table_charge_and_save(generales, "operativos", "Datos Operativos")

if __name__ == '__main__':
    main()
