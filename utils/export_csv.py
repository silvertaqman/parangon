# Función para exportar un DataFrame a un archivo CSV y devolverlo en formato binario
def export_csv(df):
    # Convierte el DataFrame a un archivo CSV con índice incluido y lo codifica en formato 'utf-8'
    return df.to_csv(index=True).encode('utf-8')