# Importación de módulos y librerías necesarios
import streamlit as st
import pandas as pd
import plotly_express as px

#crea una tabla pivote con los valores brutos
def pivot_value_table(df, index:str):
    # Realiza una copia del DataFrame de entrada para evitar cambios inesperados
    df = df.copy()
    
    # Define un diccionario que mapea columnas y operaciones de agregación
    map_for_pivot = {'cod_producto': 'count',
                     'inv_prom/bultos': 'sum',
                     'bultos_vendidos': 'sum',
                     'valor_inv_prom_bultos': 'sum',
                     'ventas_totales': 'sum',
                     'margen_bruto': 'sum',
                     'cubicaje_inv_prom': 'sum',
                     'ordenes_anual': 'sum'}
    
    # Crea una tabla dinámica utilizando pandas con las columnas y operaciones definidas
    pivot_table = pd.pivot_table(df, 
                                index=index, 
                                values=map_for_pivot.keys(),
                                aggfunc=map_for_pivot,
                                margins=True,  # Agrega una fila "Total" al final
                                margins_name="Total",
                                sort=False)  # Ordena las filas en orden alfabético por producto
                                
    # Cambia los nombres de las columnas en la tabla pivot_table
    pivot_table.columns = [f"{agg}({key})" for key, agg in map_for_pivot.items()]
    
    # Ordena las filas alfabéticamente
    pivot_table = pivot_table.sort_values(by=index)
    
    # Redondea los valores en la tabla a números enteros
    pivot_table = pivot_table.round(0)
    
    # Devuelve la tabla pivot resultante
    return pivot_table

#muestra la tabla pivote con el formato y color que deben tener
def show_pivot_value_table(pivot_table):
    # Crear el DataFrame con los estilos aplicados a las columnas
    styled_pivot_table = pivot_table.style

    # Aplicar formato a las columnas
    cubicaje_format = "{:.0f} m³"
    currency_format = "$ {:,.0f}"
    integer_format = "{:.0f}"
    styled_pivot_table = styled_pivot_table.format({
        'count(cod_producto)': integer_format,
        'sum(inv_prom/bultos)': integer_format,
        'sum(bultos_vendidos)': integer_format,
        'sum(valor_inv_prom_bultos)': currency_format,
        'sum(ventas_totales)': currency_format,
        'sum(margen_bruto)': currency_format,
        'sum(cubicaje_inv_prom)': cubicaje_format,
        'sum(ordenes_anual)': integer_format
    })
    
    # Crear un diccionario para definir los estilos de las columnas
    column_styles = {}
    
    # Iterar a través de las columnas del DataFrame y pone colores intercalados
    for idx, col in enumerate(styled_pivot_table.columns):
        if idx % 2 == 0:
            column_styles[col] = { 'color': 'Aqua'}
        else:
            column_styles[col] = { 'color': 'orange'}
    
    # Aplicar los estilos definidos a las columnas
    for column, styles in column_styles.items():
        styled_pivot_table = styled_pivot_table.set_properties(subset=column, **styles)
    
# Define una función que aplique el estilo a las filas
    def estilo_fila(s):
        return ['background-color: maroon' if s.name == "Total" else None] * len(s)

    # Aplica el estilo a las filas utilizando la función apply
    styled_pivot_table = styled_pivot_table.apply(estilo_fila, axis=1)
    
    # Mostrar el DataFrame con los estilos aplicados
    st.dataframe(styled_pivot_table, use_container_width=True)

#crea una tabla pivote con los valores porcentuales
def pivot_percent_table(df):
    # Realiza una copia del DataFrame de entrada para evitar cambios inesperados
    df = df.copy()
    
    # Cambia los nombres de las columnas del DataFrame
    df.columns = ["% Sku's","% inv prom/bult","% bult vendidos",
                  "% valor inv prom $","% ventas totales","% margen bruto",
                  "% cub inv prom","% ordenes anual"] 
    
    # Elimina la fila "Total" del DataFrame
    df.drop("Total", inplace=True)
    
    # Crea un DataFrame vacío llamado percent_table
    percent_table = pd.DataFrame()
    
    # Calcula los porcentajes de cada columna dividiendo por la suma de la columna
    for column in df.columns:
        percent_table[column] = (df[column] / df[column].sum()) 
    
    # Transpone el DataFrame para que los "Drivers" sean el índice
    percent_table = percent_table.T
    
    # Establece el nombre del índice como "Driver"
    percent_table.index.name = "Driver"
    
    # Agrega una columna "Total" que contiene la suma de los porcentajes de cada fila
    percent_table['Total'] = percent_table.sum(axis=1)
    
    # Devuelve el DataFrame con los porcentajes calculados
    return percent_table

#muestra la tabla pivote con el formato y color que deben tener
def show_pivot_percent_table(percent_table):
    # Formatea los valores en el DataFrame para mostrar los porcentajes con dos decimales
    # excepto la última columna que se muestra sin decimales
    percent_table = percent_table.style.format({col: '{:.2%}' if col != percent_table.columns[-1] else '{:.0%}' for col in percent_table.columns})
    
    # Crea un diccionario para definir los estilos de las columnas
    column_styles = {}
    
    # Itera a través de las columnas del DataFrame estilizado
    for idx, col in enumerate(percent_table.columns):
        # Alterna los colores de las columnas basado en su índice
        if idx % 2 == 0:
            column_styles[col] = { 'color': 'Aqua'}
        else:
            column_styles[col] = { 'color': 'orange'}
    
    # Aplica los estilos definidos a las columnas del DataFrame estilizado
    for column, styles in column_styles.items():
        percent_table = percent_table.set_properties(subset=column, **styles)

    # Define una función que aplique el estilo a la última columna
    def estilo_ultima_columna(s):
        estilos = ['background-color: midnightblue' if col == s.index[-1] else '' for col in s.index]
        return estilos

    # Aplica el estilo a las columnas utilizando la función apply
    percent_table = percent_table.apply(estilo_ultima_columna, axis=1)
    
    # Muestra el DataFrame estilizado utilizando Streamlit
    st.dataframe(percent_table, use_container_width=True)

# Muestra una gráfica de barras usando plotly en base a los datos de la tabla de porcentaje
def show_barchart_dataminnigdrivers(percent_produc_table):
    # Definición de una paleta de colores para usar en gráficos Plotly
    plotly_palette = [
        "steelblue", "palegoldenrod", "mediumorchid", "lightgreen", "lightcoral", "greenyellow", "gold",
        "firebrick", "deepskyblue", "darkseagreen", "darkgoldenrod", "cornflowerblue", "chartreuse", "burlywood",
        "blueviolet", "beige", "aquamarine", "aliceblue"
    ]
    # Realiza una copia del DataFrame de porcentajes de productos para evitar cambios inesperados
    percent_produc_table = percent_produc_table.copy()
    
    # Elimina la fila "Total" del DataFrame
    percent_produc_table.drop("Total", axis=1, inplace=True)
    
    # Utiliza la paleta de colores personalizada para la gráfica de barras
    colores = plotly_palette[:len(percent_produc_table.columns)]
    
    # Crea una gráfica de barras utilizando Plotly Express
    fig = px.bar(percent_produc_table, 
                x=percent_produc_table.index, 
                y=percent_produc_table.columns, 
                barmode='group',
                title='Porcentaje de drivers por categoría de producto', 
                labels={'index': 'Drivers', 'value': 'Valor (%)'}, 
                color_discrete_sequence=colores)
    
    # Formatea el eje y para mostrar valores en formato de porcentaje
    fig.update_layout( yaxis_tickformat='.0%')
    
    # Agrega etiquetas a las barras que muestran el valor en porcentaje
    fig.update_traces(
        texttemplate='%{y:.0%}',
        textposition='outside'
    )
    
    # Muestra la gráfica de barras utilizando Streamlit (representado por 'st')
    st.plotly_chart(fig, use_container_width=True)
