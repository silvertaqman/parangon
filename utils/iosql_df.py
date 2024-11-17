import streamlit as st
import data.db as db

def create_table_charge_and_save(obj, attribute_key, title, format=None):
    """
    Crea una tabla interactiva para editar y guardar parámetros usando un objeto.

    Args:
        obj (object): Instancia de la clase que contiene los atributos.
        attribute_key (str): Nombre del atributo del objeto a modificar.
        title (str): Título de la sección.
        format (str, optional): Formato esperado de los valores. Default: None.
    """
    st.subheader(title)
    
    # Obtener la lista de parámetros del atributo del objeto
    param_list = getattr(obj, attribute_key, [])
    
    # Crear campos de entrada para cada parámetro
    updated_params = []
    for param in param_list:
        if format:
            value = st.text_input(
                param, key=f"{attribute_key}_{param}", help=f"Enter value in {format} format"
            )
        else:
            value = st.text_input(param, key=f"{attribute_key}_{param}")
        updated_params.append(value)
    
    # Guardar los parámetros en el objeto
    if st.button(f"Guardar {title}", key=f"save_button_{attribute_key}"):
        setattr(obj, attribute_key, updated_params)
        st.success(f"{title} guardados exitosamente!")
        
        # Guardar en la base de datos
        username = st.session_state.get("username", "default_user")
        user = db.fetch_user(username)
        if user:
            parameters = user.get('parameters', {})
            parameters[attribute_key] = updated_params
            if db.update_user(username, {'parameters': parameters}):
                st.success(f"{title} guardados en la base de datos.")
            else:
                st.error("Error al guardar los datos en la base de datos.")
        else:
            st.error(f"Error: Usuario {username} no encontrado en la base de datos.")
