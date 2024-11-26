import streamlit as st
from utils.export_df import *
from utils.structure_df import TransformDF, GeneratedDF
import pandas as pd

def get_styled_dataframe(df_transformed):
    # Aplica estilos al DataFrame transformado utilizando la función 'style_dataframe'
    expected_columns = TransformDF().expected_columns
    calculados = GeneratedDF()
    df_styled = calculados.style_df(df_transformed, expected_columns)
    
    # Devuelve el DataFrame con estilos aplicados
    return df_styled

# Función para mostrar botones de descarga de datos en una aplicación Streamlit
def download_dataframe(df, name="Base"):
    # Exporta el DataFrame a formatos CSV y Excel
    csv = export_csv(df)
    excel = export_excel(df)

    # Muestra una leyenda en la aplicación Streamlit
    st.caption("Exportar datos:")
    
    # Crea botones de descarga para CSV y Excel en la aplicación Streamlit
    st.download_button(
        label="Descargar como CSV",
        data=csv,
        file_name=f'{name}.csv'
    )

    st.download_button(
        label="Descargar como Excel",
        data=excel,
        file_name=f'{name}.xlsx'
    )
