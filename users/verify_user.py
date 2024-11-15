import streamlit as st
from config.confloader import get_db_connection

def verify_user(username, password):
    try:
        connection = get_db_connection()
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
            return stored_password_hash == hash_password(password)
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
