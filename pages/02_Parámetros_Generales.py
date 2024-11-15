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

def create_table_charge_and_save(param_list, param_key, title, format=None):
    st.subheader(title)
    
    # Get the current parameters
    current_params = st.session_state.get('parameters', {}).get(param_key, [])
    
    # Create a dictionary from the current parameters
    param_dict = {param['name']: param['value'] for param in current_params}
    
    # Create input fields for each parameter
    updated_params = []
    for param in param_list:
        if format:
            value = st.text_input(param, value=param_dict.get(param, ""), key=f"{param_key}_{param}", 
                                  help=f"Enter value in {format} format")
        else:
            value = st.text_input(param, value=param_dict.get(param, ""), key=f"{param_key}_{param}")
        updated_params.append({"name": param, "value": value})
    
    # Save button with a unique key
    if st.button(f"Guardar {title}", key=f"save_button_{param_key}"):
        st.session_state.parameters = st.session_state.get('parameters', {})
        st.session_state.parameters[param_key] = updated_params
        
        # Save to database
        username = st.session_state["username"]
        user = db.fetch_user(username)
        if user is not None:
            # Update only the specific parameter key
            parameters = user.get('parameters', {})
            parameters[param_key] = updated_params
            if db.update_user(username, {'parameters': parameters}):
                st.success(f"{title} guardados exitosamente!")
            else:
                st.error("Error al guardar los datos en la base de datos.")
        else:
            st.error(f"Error: User {username} not found in the database.")

def main():
    # Comprueba el estado de autenticación del usuario
    if st.session_state["authentication_status"] is False:
        st.error('Usuario/contraseña incorrecto')
    elif st.session_state["authentication_status"] is None:
        st.warning('Por favor ingresa tu usuario y contraseña')
    elif st.session_state["authentication_status"]:
        # Si la autenticación es exitosa, muestra el contenido principal
        
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
        inv_inversiones_calculado  = param_names["inventario"]["inversiones_calculado"]

        gen_financieros = param_names["generales"]["financieros"]
        gen_financieros_calculados = param_names["generales"]["financieros_calculados"]
        gen_operativos = param_names["generales"]["operativos"]

        # Crear pestañas para diferentes conjuntos de parámetros: Almacenaje, Inventario y Generales
        tab1, tab2, tab3 = st.tabs(["Parámetros Almacenaje", "Parámetros Inventario", "Parámetros Generales"])

        # Fetch parameters from the database
        param_res = db.fetch_user(st.session_state["username"])
        
        # Initialize parameters with default empty values
        parameters = initialize_default_parameters()

        # Update parameters if they exist in the database
        if isinstance(param_res, dict) and "parameters" in param_res:
            parameters.update(param_res["parameters"])
        else:
            st.warning("El usuario no tiene parámetros. Se usarán valores predeterminados.")

        # Dentro de la pestaña "Parámetros Almacenaje"
        with tab1:
            create_table_charge_and_save(alm_datos, "alm_datos", "Datos")
            st.divider()
            create_table_charge_and_save(alm_costosgastos, "alm_costosgastos", "Costos y gastos")
            st.divider()
            create_table_charge_and_save(alm_inversiones, "alm_inversiones", "Inversiones")

        # Dentro de la pestaña "Parámetros Inventario"
        with tab2:
            # Ensure that inv_datos_calculados and parameters["inv_datos_calculados"] have the same length
            inv_datos_calculados_values = parameters.get("inv_datos_calculados", [])
            if len(inv_datos_calculados) != len(inv_datos_calculados_values):
                # If lengths don't match, create a new list with default values
                inv_datos_calculados_values = [{"name": param, "value": ""} for param in inv_datos_calculados]
            
            backend.parameter_table("Datos", inv_datos_calculados, inv_datos_calculados_values)
            create_table_charge_and_save(inv_datos, "inv_datos", "Datos")
            st.divider()
            create_table_charge_and_save(inv_costosgastos, "inv_costosgastos", "Costos y gastos")
            st.divider()
            
            # Similar adjustment for inv_inversiones_calculado
            inv_inversiones_calculado_values = parameters.get("inv_inversiones_calculado", [])
            if len(inv_inversiones_calculado) != len(inv_inversiones_calculado_values):
                inv_inversiones_calculado_values = [{"name": param, "value": ""} for param in inv_inversiones_calculado]
            
            backend.parameter_table("Inversiones", inv_inversiones_calculado, inv_inversiones_calculado_values)
            create_table_charge_and_save(inv_inversiones, "inv_inversiones", "Inversiones")

        # Dentro de la pestaña "Parámetros Generales"
        with tab3:
            gen_financieros_calculados_values = parameters.get("gen_financieros_calculados", [])
            
            # Ensure both lists have the same length
            max_length = max(len(gen_financieros_calculados), len(gen_financieros_calculados_values))
            gen_financieros_calculados = gen_financieros_calculados[:max_length] + [''] * (max_length - len(gen_financieros_calculados))
            gen_financieros_calculados_values = gen_financieros_calculados_values[:max_length] + [{'name': '', 'value': ''}] * (max_length - len(gen_financieros_calculados_values))
            
            backend.parameter_table("Financieros", gen_financieros_calculados, gen_financieros_calculados_values)
            create_table_charge_and_save(gen_financieros, "gen_financieros", "Financieros", format="%")
            st.divider()
            create_table_charge_and_save(gen_operativos, "gen_operativos", "Operativos")

        # Obtener información del usuario desde la base de datos y realizar cálculos en función de esa información
        response = db.get_drive(st.session_state["username"])
        if response is not None:
            backend.calculated_params(response, {"parameters": parameters})
        else:
            st.warning("Por favor, cargue sus datos primero.")

def initialize_default_parameters():
    # Define default values for all your parameters
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

if __name__ == '__main__':
    main()
