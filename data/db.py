import psycopg2
from psycopg2 import sql
import logging
import os
import bcrypt
import json
from psycopg2.extras import Json
from config.confloader import load_config, get_db_config, get_db_connection

#env_settings = load_config()
DISK_MOUNT_PATH = '/mnt/volume'
# Cargar configuraciones desde YAML o .env

# Nota: Las funciones relacionadas con archivos (create_drive y get_drive) 
# necesitarán una solución diferente, ya que PostgreSQL no maneja archivos directamente.
# Podrías considerar usar un sistema de archivos separado o un servicio de almacenamiento en la nube.

def create_drive(username, file):
    file_name = f"{username}/table.xlsx"
    file_path = os.path.join(DISK_MOUNT_PATH, file_name)

    # Crea el directorio si no existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Guarda el archivo en el disco montado
    with open(file_path, 'wb') as f:
        f.write(file.read())
        
    return file_path  # Devuelve la ruta del archivo guardado

def get_drive(username):
    file_name = f"{username}/table.xlsx"
    file_path = os.path.join(DISK_MOUNT_PATH, file_name)

    # Verifica si el archivo existe antes de intentar leerlo
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()  # Devuelve los datos binarios del archivo
    else:
        return None

# Las funciones para manejo de usuario se mantienen
def insert_user(username, name, email, parameters, password, drivers):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, name, email, parameters, password, drivers) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING username",
                (username, name, email, parameters, hashed_password, drivers)
            )
            conn.commit()
            return cur.fetchone()[0]

def fetch_all_users():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, name, email, password FROM users")
                users = cur.fetchall()
                return {
                    "usernames": {user[0]: {
                        "email": user[2],
                        "name": user[1],
                        "password": user[3]
                    } for user in users}
                }
    except Exception as e:
        logging.error(f"Error in fetch_all_users: {e}")
        raise


def fetch_user(username):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user_data = cur.fetchone()
            if user_data:
                # Convert tuple to dictionary
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, user_data))
    return None

def get_user(username):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cur.fetchone()

def update_user(username, updates):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Convert any dictionary values to JSON
            for key, value in updates.items():
                if isinstance(value, dict):
                    updates[key] = Json(value)
            
            query = sql.SQL("UPDATE users SET {} WHERE username = %s").format(
                sql.SQL(', ').join(sql.SQL("{}=%s").format(sql.Identifier(k)) for k in updates.keys())
            )
            cur.execute(query, list(updates.values()) + [username])
            conn.commit()
    return True

def delete_user(username):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE username = %s", (username,))

def update_password_to_bcrypt(username: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (hashed_password, username)
            )
            conn.commit()