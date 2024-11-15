# Importar las bibliotecas necesarias
import streamlit as st
import json
from utils import backend
import data.db as db

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)

def initialize_default_parameters():
    """
    Inicializa valores predeterminados para los parámetros.
    """
    return {
        "alm_datos": [],
        "alm_costosgastos": [],
        "alm_inversiones": [],
        "inv_datos": [],
        "inv_datos_calculados": [],
        "inv_costosgastos": [],
        "inv_inversiones": [],
        "inv_inversiones_calculado": [],
        "gen_financieros": [],
        "gen_financieros_calculados": [],
        "gen_operativos": []
    }

def create_table_charge_and_save(param_list, param_key, title, format=None):
    """
    Crea una tabla interactiva para editar y guardar parámetros en Streamlit.
    
    Args:
        param_list (list): Lista de nombres de parámetros.
        param_key (str): Clave para identificar el conjunto de parámetros en session_state.
        title (str): Título de la sección.
        format (str, optional): Formato esperado de los valores (para propósitos de ayuda). Default: None.
    """
    st.subheader(title)
    
    # Obtener los parámetros actuales de session_state
    current_params = st.session_state.get('parameters', {}).get(param_key, [])
    param_dict = {param['name']: param['value'] for param in current_params}
    
    # Crear campos de entrada para cada parámetro
    updated_params = []
    for param in param_list:
        if format:
            value = st.text_input(
                param, value=param_dict.get(param, ""), 
                key=f"{param_key}_{param}", help=f"Enter value in {format} format"
            )
        else:
            value = st.text_input(param, value=param_dict.get(param, ""), key=f"{param_key}_{param}")
        updated_params.append({"name": param, "value": value})
    
    # Botón para guardar
    if st.button(f"Guardar {title}", key=f"save_button_{param_key}"):
        st.session_state.parameters = st.session_state.get('parameters', {})
        st.session_state.parameters[param_key] = updated_params
        st.success(f"{title} guardados exitosamente!")

def main():
    """
    Función principal para cargar, editar y guardar tablas interactivas.
    """
    # Leer el contenido del archivo JSON que contiene nombres de parámetros
    with open('json_files/param_names.json', 'r') as archivo_json:
        param_names = json.load(archivo_json)

    # Variables con las listas correspondientes
    alm_datos = param_names["almacenaje"]["datos"]
    alm_costosgastos = param_names["almacenaje"]["costos_gastos"]
    alm_inversiones = param_names["almacenaje"]["inversiones"]

    inv_datos = param_names["inventario"]["datos"]
    inv_datos_calculados = param_names["inventario"]["datos_calculados"]
    inv_costosgastos = param_names["inventario"]["costos_gastos"]
    inv_inversiones = param_names["inventario"]["inversiones"]
    inv_inversiones_calculado = param_names["inventario"]["inversiones_calculado"]

    gen_financieros = param_names["generales"]["financieros"]
    gen_financieros_calculados = param_names["generales"]["financieros_calculados"]
    gen_operativos = param_names["generales"]["operativos"]

    # Crear pestañas para diferentes conjuntos de parámetros
    tab1, tab2, tab3 = st.tabs(["Parámetros Almacenaje", "Parámetros Inventario", "Parámetros Generales"])

    # Inicializar valores predeterminados
    parameters = initialize_default_parameters()

    # Pestaña "Parámetros Almacenaje"
    with tab1:
        create_table_charge_and_save(alm_datos, "alm_datos", "Datos")
        st.divider()
        create_table_charge_and_save(alm_costosgastos, "alm_costosgastos", "Costos y gastos")
        st.divider()
        create_table_charge_and_save(alm_inversiones, "alm_inversiones", "Inversiones")

    # Pestaña "Parámetros Inventario"
    with tab2:
        create_table_charge_and_save(inv_datos, "inv_datos", "Datos")
        st.divider()
        create_table_charge_and_save(inv_costosgastos, "inv_costosgastos", "Costos y gastos")
        st.divider()
        create_table_charge_and_save(inv_inversiones, "inv_inversiones", "Inversiones")

    # Pestaña "Parámetros Generales"
    with tab3:
        create_table_charge_and_save(gen_financieros, "gen_financieros", "Financieros", format="%")
        st.divider()
        create_table_charge_and_save(gen_operativos, "gen_operativos", "Operativos")

if __name__ == '__main__':
    main()
