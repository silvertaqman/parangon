import streamlit as st
import pandas as pd
import transform_dataframe
# Función para obtener un DataFrame transformado a partir de una tabla Excel
def get_transformed_dataframe(table):
    if table is None:
        st.warning("No hay datos disponibles para transformar.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Read the Excel file and load its contents into a DataFrame
    df = pd.read_excel(table, engine='openpyxl')
    
    # Apply a transformation function (transform_dataframe) to the DataFrame
    df_transformed = transform_dataframe(df)
    
    # Return the transformed DataFrame
    return df_transformed