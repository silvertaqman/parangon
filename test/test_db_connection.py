#Esto es un ejemplo de como conectar a la base de datos en aiven
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
