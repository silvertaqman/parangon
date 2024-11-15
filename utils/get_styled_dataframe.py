import style_dataframe
# Función para obtener un DataFrame con estilos a partir de un DataFrame transformado
def get_styled_dataframe(df_transformed):
    # Aplica estilos al DataFrame transformado utilizando la función 'style_dataframe'
    df_styled = style_dataframe(df_transformed)
    
    # Devuelve el DataFrame con estilos aplicados
    return df_styled