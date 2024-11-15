from typing import Dict
import yaml
from decouple import config

# Define el path al archivo YAML de configuración
PATH_CONFIG_YAML = config('PATH_CONFIG_YAML', default='config/config.yaml')

def load_config() -> Dict[str, str]:
    """
    Carga y retorna la configuración de la aplicación desde un archivo YAML,
    dependiendo del entorno especificado en la variable APP_ENV.
    """
    # Determina el entorno actual, por defecto 'default'
    ENV = config('APP_ENV', default='default')

    # Carga la configuración desde el archivo YAML
    with open(PATH_CONFIG_YAML, "r") as file:
        config_data = yaml.safe_load(file)

    # Configuración específica para el entorno
    env_config = config_data.get(ENV, {})

    # Reemplaza valores de placeholders con las variables de entorno
    for key, value in env_config.items():
        env_config[key] = config(value, default=value)

    return env_config

def get_db_config(env_settings: Dict[str, str]) -> Dict[str, str]:
    """
    Extrae y retorna la configuración de la conexión a PostgreSQL desde
    el diccionario de configuración general.
    """
    return {
        'dbname': env_settings.get('DBNAME'),
        'user': env_settings.get('DBUSER'),
        'password': env_settings.get('DBPASSWORD'),
        'host': env_settings.get('DBHOST'),
        'port': env_settings.get('DBPORT')
    }


def get_db_connection():
    return psycopg2.connect(**db_config)
