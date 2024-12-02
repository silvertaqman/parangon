# Importar las bibliotecas necesarias
import streamlit as st
from utils import backend
import database
import json

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)

if not st.session_state.get("data_ready", False):
    st.error("Los datos no están disponibles. Completa el proceso de ingreso de datos para acceder a esta página.")
    st.stop()
def main():
    # Comprueba el estado de autenticación del usuario
    if st.session_state["authentication_status"] is False:
        # Muestra un mensaje de error si la autenticación es incorrecta
        st.error('Usuario/contraseña incorrecto')
    elif st.session_state["authentication_status"] is None:
        # Muestra un mensaje de advertencia si aún no se ha ingresado usuario y contraseña
        st.warning('Por favor ingresa tu usuario y contraseña')
    elif st.session_state["authentication_status"]:
        # Si la autenticación es exitosa, muestra el contenido principal

        # Obtener la información del usuario desde la base de datos.
        drive_res = database.get_drive(st.session_state["username"])
        res = database.fetch_user(st.session_state["username"])

        # Obtener los parámetros y drivers del usuario desde la base de datos.
        parameters = res["parameters"]
        drivers = res["drivers"]

        # Transformar los datos y crear tablas de valor y porcentaje.
        df_transformed = backend.get_transformed_dataframe(drive_res)
        value_produc_table = backend.pivot_value_table(df_transformed, 'cat_producto')
        percent_produc_table = backend.pivot_percent_table(value_produc_table)

        # Cargar los nombres de los parámetros desde un archivo JSON.
        with open('json_files/param_names.json', 'r') as archivo_json:
            param_names = json.load(archivo_json)
        
        # Definir una función para calcular y mostrar el scorecard.
        def scorecard(percent_produc_table, table_name, inver_param_names, cost_param_names,
                    inver_param_values, cost_param_values, capital_cost_value, drivers_key):
            # Calcular el scorecard completo.
            df_scorecard_all = backend.scorecard_all(percent_produc_table,
                                                    table_name=table_name,
                                                    inver_param_names=inver_param_names,
                                                    inver_param_values=inver_param_values,
                                                    capital_cost_value=capital_cost_value,
                                                    cost_param_names=cost_param_names,
                                                    cost_param_values=cost_param_values)

            # Mostrar el scorecard en una tabla con la opción de guardar cambios.
            scorecard = backend.show_scorecard(percent_produc_table,
                                            table_name=table_name,
                                            inver_param_names=inver_param_names,
                                            cost_param_names=cost_param_names,
                                            drivers_list=drivers["categorias"][drivers_key],
                                            df_scorecard_all=df_scorecard_all)

            # Definir una función para guardar los cambios realizados en el scorecard.
            def save():
                drivers["categorias"][drivers_key] = scorecard["Drivers"].to_list()[:-1]
                database.update_user(username=st.session_state["username"], updates={"drivers": drivers})

            st.button("Calcular", on_click=save, key=drivers_key)

            # Verificar si se realizaron cambios en los controladores y mostrar una advertencia si es necesario.
            if scorecard["Drivers"].to_list()[:-1] != drivers["categorias"][drivers_key]:
                st.warning("""Haz click en "Calcular" para efectuar los cambios""")
                st.toast("Tienes cambios pendientes", icon='❗')

            return scorecard

        # Sección para mostrar el scorecard de "Costos del almacén".
        with st.expander("Costos del almacén"):
            tab_1, tab_2 = st.tabs(["Tabla 📄","Exportar 📁"])
            with tab_1:
                params_json = json.dumps(parameters)
                alm_scorecard = backend.scorecard_all(
                percent_produc_table=percent_produc_table.drop("Total", axis=1),
                table_name="Costos del almacén",
                params_json=params_json,
                capital_cost_value = float(parameters["gen_financieros"][0]["value"]))
        
            with tab_2:
                backend.download_dataframe(alm_scorecard, name="scorecard_cost_almacen_cat")

        # Sección para mostrar el scorecard de "Costos del inventario".
        with st.expander("Costos del inventario"):
            tab_1, tab_2 = st.tabs(["Tabla 📄","Exportar 📁"])
            with tab_1:
                inv_scorecard = scorecard(percent_produc_table.drop("Total", axis=1),
                    table_name="Costos del inventario",
                    inver_param_names=param_names["inventario"]["inversiones"],
                    cost_param_names=param_names["inventario"]["inversiones_calculado"][1:] + param_names["inventario"]["costos_gastos"],
                    inver_param_values=parameters["inv_inversiones"],
                    cost_param_values=parameters["inv_inversiones_calculado"][1:] + parameters["inv_costosgastos"],
                    capital_cost_value=parameters["gen_financieros"][0],
                    drivers_key="inv_drivers")
            with tab_2:
                backend.download_dataframe(inv_scorecard, name="scorecard_cost_invent_cat")

        # Sección para mostrar el scorecard de "Costo total y KPI's".
        with st.expander("Costo total y KPI's"):
            tab_1, tab_2 = st.tabs(["Tabla 📄","Exportar 📁"])
            with tab_1:
                total_cost_df = backend.total_scorecard(alm_scorecard, inv_scorecard, value_produc_table)
                st.session_state["total_scorecard_cat"] = total_cost_df
            with tab_2:
                backend.download_dataframe(total_cost_df, name="scorecard_cost_total_cat")

        # Mostrar un gráfico de barras horizontales con los costos de almacén e inventario.
        backend.horizontal_bar_chart(alm_scorecard, inv_scorecard)

        # Mostrar un gráfico de barras verticales con el costo total por categoría.
        backend.vertical_chart_value(total_cost_df)

        # Mostrar un gráfico de barras verticales con la tasa de mantener el inventario (ICR) por categoría.
        backend.vertical_chart_percent(total_cost_df)

if __name__ == '__main__':
    main()

