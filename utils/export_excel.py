import pandas as pd
import io
# Función para exportar un DataFrame a un archivo Excel y devolverlo en formato binario
def export_excel(df):
    # Crea un objeto de salida en formato binario
    output = io.BytesIO()
    
    # Crea un escritor de Excel utilizando el motor 'openpyxl'
    writer = pd.ExcelWriter(output, engine='openpyxl')
    
    # Guarda el DataFrame en una hoja de Excel llamada 'Base transformada' con índice incluido
    df.to_excel(writer, sheet_name='Base transformada', index=True)
    
    # Cierra el escritor y ajusta la posición del objeto de salida al principio
    writer.close()
    output.seek(0)
    
    # Devuelve el objeto de salida en formato binario
    return output
