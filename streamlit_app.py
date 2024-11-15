import streamlit as st
from utils import backend
import psycopg2
from config.confloader import load_config, get_db_config
import pandas as pd
import logging

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Cargar toda la configuración
try:
    env_settings = load_config()
    #print(f"Configuración cargada: {env_settings}")
except Exception as e:
    logging.error(f"Error al cargar la configuración: {e}")
    raise

# Obtener la configuración específica de PostgreSQL
db_config = get_db_config(env_settings)

# Initialize connection.
conn = psycopg2.connect(
    dbname=db_config['dbname'],
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port']
)
# Perform query.
query = 'SELECT * FROM almacenaje;'
with conn.cursor() as cursor:
    cursor.execute(query)
    # Obtiene los resultados y conviértelos en un DataFrame
    columns = [desc[0] for desc in cursor.description]  # Obtener nombres de columna
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)

# Cierra la conexión
conn.close()

# Imprime los resultados
for row in df.itertuples():
    st.write(f"{row.numero_personas_almacen} personas y {row.metros_cuadrados_almacen} metros cuadrados")
