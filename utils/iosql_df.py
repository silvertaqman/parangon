import streamlit as st
import pandas as pd
from config.confloader import get_db_connection

# Configuración del modelo, vista y controlador
class Model:
    """
    Modelo que representa la estructura de los datos.
    """
    def __init__(self, table_name):
        self.table_name = table_name

    def save_to_db(self, df):
        """
        Guarda un DataFrame en la tabla correspondiente de PostgreSQL.
        """
        try:
            with get_db_connection() as conn:
                # Inserta filas del DataFrame en la base de datos
                for _, row in df.iterrows():
                    query = f"INSERT INTO {self.table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(row))})"
                cursor = conn.cursor()
                cursor.execute(query, tuple(row))
                conn.commit()
                cursor.close()
                conn.close()
            return "Datos guardados exitosamente en la base de datos."
        except Exception as e:
            return f"Error al guardar en la base de datos: {str(e)}"

class View:
    """
    Vista que gestiona la interfaz de usuario.
    """
    def display_form(self, columns, table_name):
        """
        Muestra cuadros de entrada para los valores del DataFrame.
        """
        st.header(f"Formulario para {table_name}")
        data = {}
        for col in columns:
            value = st.text_input(f"{col}", key=f"input_{col}")
            data[col] = value
        return data

    def display_confirmation(self, message):
        """
        Muestra mensajes de éxito o error.
        """
        if "Error" in message:
            st.error(message)
        else:
            st.success(message)

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def validate_data(self, data):
        """
        Valida los datos ingresados por el usuario.
        """
        return all(data.values())  # Ejemplo: Asegurarse de que todos los campos estén llenos

    def save_data(self, data):
        """
        Guarda los datos en la base de datos.
        """
        try:
            df = pd.DataFrame([data])  # Crear DataFrame a partir de los datos
            return self.model.save_to_db(df)  # Guardar usando el modelo
        except Exception as e:
            return f"Error al guardar los datos: {str(e)}"


# Clase para guardar nombres de parametros (reemplaza json database y params)
class Almacenaje:
    def __init__(self):
        self.datos = [
            "Número de personas almacén",
            "Metros cuadrados del almacén",
            "Número de equipos",
            "Número de posiciones",
            "Otros gastos de almacén"
        ]
        self.costos_gastos = [
            "Costo mano de obra anual $",
            "Costo del alquiler del almacén $",
            "Costo suministros de oficina $",
            "Costos de energía (electricidad, gas, otros) $",
            "Servicios de terceros en logística (3PL) $",
            "Otros gastos $"
        ]
        self.inversiones = [
            "Inversiones en edificio y terreno $",
            "Sistema de manejo de materiales (montacargas, elevadores, carretillas, baterías, etc) $",
            "Sistemas de almacenamiento (Racks, Conveyors, carretillas, etc) $",
            "WMS (licencias, mantenimiento, etc) $",
            "Seguros del inventario $",
            "Otras inversiones $"
        ]

    def calcular_total_costos(self, costos):
        """Ejemplo de cálculo basado en costos."""
        return sum(costos)

class Inventario:
    def __init__(self):
        self.datos = [
            "Número de personas dedicadas al control de inventario (encargados y planeadores)",
            "Metros cuadrados de oficinas inventarios",
            "Número de equipos (fax, computadoras, etc)"
        ]
        self.costos_gastos = [
            "Costos de mano de obra de personas dedicadas al control de inventario $",
            "Costos de energía de la oficina de inventarios $",
            "Suministros de oficina de inventarios $",
            "Costos de espacio de oficina de inventarios $",
            "Otros gastos de la oficina de inventarios $"
        ]
        # Más atributos...

    def calcular_inversion_total(self, inversiones):
        """Ejemplo de cálculo basado en inversiones."""
        return sum(inversiones)

class Generales:
    def __init__(self):
        self.financieros = ["Costo de capital de la empresa %"]
        self.operativos = ["Número de horas laborales anual FTE"]
        # Más atributos...

    def obtener_financieros(self):
        """Ejemplo de funcionalidad específica."""
        return self.financieros

# Clase para almacenar valores ingresados en parametros
