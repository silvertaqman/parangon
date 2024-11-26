import psycopg2
from psycopg2 import sql
import logging
import os
import bcrypt
import json
from psycopg2.extras import Json
from config.confloader import get_db_connection

# Las funciones para manejo de usuario se mantienen
def insert_user(username, name, email, parameters, password, drivers):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (id,username,password_hash,email,created_at,name) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING username",
                (id, username, password_hash, email, created_at, name)
            )
            conn.commit()
            return cur.fetchone()[0]

def fetch_all_users():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, name, email, password_hash FROM users")
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