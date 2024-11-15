import json
# Función para aplicar estilos y formato a un DataFrame
def style_dataframe(df):
    df = df.copy()  # Realiza una copia del DataFrame original para no modificarlo

    # ruta al JSON que contiene los nombres de las columnas
    json_filename = 'json_files/database_names.json'
    
    # Carga el contenido del archivo JSON en un diccionario
    with open(json_filename, 'r') as json_file:
        data_dictionary = json.load(json_file)

    # Divide las columnas del DataFrame en dos grupos: esperadas y calculadas
    expected_columns = data_dictionary['expected_columns']
    calculated_columns = data_dictionary['calculated_columns']

    # Define los estilos para cada grupo de columnas
    column_styles = {
        col: {'background-color': 'black', 'color': 'lawngreen'} for col in expected_columns
    }
    column_styles.update({
        col: {'background-color': 'black', 'color': 'red'} for col in calculated_columns
    })

    # Crea una copia del DataFrame con los estilos aplicados
    styled_df = df.style

    # Aplica formato a columnas específicas del DataFrame
    cubicaje_format = "{:.2f} m³"
    currency_format = "$ {:,.2f}"
    integer_format = "{:.0f}"
    percent_format = "{:.0%}"  
    decimal_format = "{:.2f}"

    styled_df = styled_df.format({
        'cubicaje/tarima': cubicaje_format,
        'cubicaje_inv_prom': cubicaje_format,
        'precio_uni/bulto': currency_format,
        'costo_uni/bulto': currency_format,
        'ventas_totales': currency_format,
        'ventas_al_costo': currency_format,
        'margen_bruto': currency_format,
        'valor_inv_prom_bultos': currency_format,
        'empaque': integer_format,
        'bultos/tarima': integer_format,
        'demanda_mes1': integer_format,
        'demanda_mes2': integer_format,
        'demanda_mes3': integer_format,
        'demanda_mes4': integer_format,
        'demanda_mes5': integer_format,
        'demanda_mes6': integer_format,
        'demanda_mes7': integer_format,
        'demanda_mes8': integer_format,
        'demanda_mes9': integer_format,
        'demanda_mes10': integer_format,
        'demanda_mes11': integer_format,
        'demanda_mes12': integer_format,
        't_entrega_prom': integer_format,
        'inv_final/bultos': integer_format,
        'inv_prom/bultos': integer_format,
        'inv_trans/bultos': integer_format,
        'unidades_vendidas': integer_format,
        'bultos_vendidos': integer_format,
        'prom_bultos_desp/mes': integer_format,
        'factor_escazes': percent_format,
        'margen_utilidad/ventas': percent_format,
        'rotacion': decimal_format,
        'meses_inv': decimal_format
    })
    
    # Aplica estilos a las columnas basados en los grupos definidos
    for column, styles in column_styles.items():
        styled_df = styled_df.set_properties(subset=column, **styles)
    
    # Devuelve el DataFrame con estilos y formato aplicados
    return styled_df