
#------------------------------------------------
# La funcion transform_dataframe puede vectorizarse para ahorrar espacio
#------------------------------------------------
def transform_dataframe(df):
    # Crear una copia del DataFrame para mantener el original sin cambios
    df_copy = df.copy()
    
    # Definir columnas de demanda mensual solo una vez
    demand_cols = [f'demanda_mes{i}' for i in range(1, 13)]
    
    # Variables auxiliares
    precio = df['precio_uni/bulto']
    costo = df['costo_uni/bulto']
    demanda = df[demand_cols]
    
    # Calcular todas las nuevas columnas de forma vectorizada
    df_copy['unidades_vendidas'] = demanda.sum(axis=1)
    df_copy['bultos_vendidos'] = df_copy['unidades_vendidas'] / df['empaque']
    df_copy['margen_utilidad/ventas'] = (precio - costo) / precio
    df_copy['ventas_totales'] = df_copy['bultos_vendidos'] * precio
    df_copy['ventas_al_costo'] = df_copy['bultos_vendidos'] * costo
    df_copy['margen_bruto'] = df_copy['bultos_vendidos'] * (precio - costo)
    df_copy['valor_inv_prom_bultos'] = df['inv_prom/bultos'] * costo
    df_copy['rotacion'] = df_copy['ventas_al_costo'] / df_copy['valor_inv_prom_bultos']
    df_copy['meses_inv'] = 12 / df_copy['rotacion']
    df_copy['prom_bultos_desp/mes'] = demanda.mean(axis=1)
    df_copy['cubicaje_inv_prom'] = df['cubicaje/tarima'] * (df['inv_final/bultos'] / df['bultos/tarima'])
    
    return df_copy
#------------------------------------------------
# No he realizado mas cambios, pero escojo el codigo minimo para correr el calculo
#------------------------------------------------