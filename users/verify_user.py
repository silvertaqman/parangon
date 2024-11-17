import streamlit as st
import bcrypt
from config.confloader import get_db_connection

def verify_user(username, password, db_config):
    """
    Verifica si un usuario existe en la base de datos y si la contraseña proporcionada coincide con la almacenada (hasheada con bcrypt).
    """
    try:
        # Conectarse a la DB
        connection = get_db_connection(db_config)
        cursor = connection.cursor()

        # Verificar usuario en la base de datos en PSQL/Aiven
        query = "SELECT password_hash FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            # Comparar hash de la contraseña ingresada
            stored_password_hash = result[0]
            # Comparar la contraseña ingresada con el hash almacenado
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return True
        return False
    except Exception as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return False

"""
# Crear un hash (password encriptado) para cada usuario que ingresa
# Debe hacerse para cada nuevo usuario
import bcrypt
def generate_password_hash(password):
    # Convertir la contraseña en bytes y generar el hash
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')  # Devolver el hash como cadena para almacenarlo

# Ejemplo de uso
password = "mypassword"
hashed_password = generate_password_hash(password)
print("Hashed password:", hashed_password)
"""
