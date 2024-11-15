import streamlit as st
import export_csv
import export_excel
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
