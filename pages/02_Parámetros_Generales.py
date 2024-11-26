import streamlit as st
import data.db as db
from utils.iosql_df import Almacenaje, Inventario, Generales, Model, View, Controller

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
    # Configurar pestaña "Almacenaje"
    with tab1:
        # Crear el modelo, vista y controlador
        model = Model(table_name="almacenaje")
        view = View()
        controller = Controller(model, view)

        # Mostrar formulario y procesar datos
        columns = almacenaje.datos  # Suponiendo que devuelve una lista de columnas
        user_data = view.display_form(columns, model.table_name)  # Mostrar formulario y obtener datos

        if st.button("Guardar datos"):
            if controller.validate_data(user_data):  # Validar datos ingresados
                message = controller.save_data(user_data)  # Guardar datos en la BD
                view.display_confirmation(message)
            else:
                view.display_confirmation("El formato de los datos es incorrecto.")



        #create_table_charge_and_save(almacenaje, "datos", "Datos Almacenaje")
        #create_table_charge_and_save(almacenaje, "costos_gastos", "Costos y Gastos Almacenaje")
        #create_table_charge_and_save(almacenaje, "inversiones", "Inversiones Almacenaje")

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
