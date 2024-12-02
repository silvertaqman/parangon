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

    def save_to_db(self, df, config):
        """
        Guarda un DataFrame en la tabla correspondiente de PostgreSQL.
        """
        try:
            with get_db_connection(config) as conn:
                # Inserta filas del DataFrame en la base de datos
                for _, row in df.iterrows():
                    query = f"INSERT INTO {self.table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
                    # st.write(query) desactiva para ver la forma de la query
                    cursor = conn.cursor()
                    cursor.execute(query, tuple(row.tolist()))
                    conn.commit()
            return "Datos guardados exitosamente en la base de datos."
        except Exception as e:
            return f"Error al guardar en la base de datos: {str(e)}"
    
    # Función para recolectar datos de una pestaña
    def recolectar_datos(columns, section_key):
        data = {}
        for key, label in columns.items():
            data[key] = st.text_input(f"{label}:", key=f"{section_key}_{key}")  # Inputs únicos
        return data

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

    def save_data(self, data, config):
        """
        Guarda los datos en la base de datos.
        """
        try:
            df = pd.DataFrame([data])  # Crear DataFrame a partir de los datos
            return self.model.save_to_db(df, config)  # Guardar usando el modelo
        except Exception as e:
            return f"Error al guardar los datos: {str(e)}"


class Almacenaje:
    def __init__(self):
        # Mapeo para datos
        self.datos = {
            "numero_personas_almacen": "Número de personas almacén",
            "metros_cuadrados_almacen": "Metros cuadrados del almacén",
            "numero_equipos": "Número de equipos",
            "numero_posiciones": "Número de posiciones",
            "otros_gastos_almacen": "Otros gastos de almacén"
        }
        
        # Mapeo para costos y gastos
        self.costos_gastos = {
            "costo_mano_obra_anual": "Costo mano de obra anual $",
            "costo_alquiler_almacen": "Costo del alquiler del almacén $",
            "costo_suministros_oficina": "Costo suministros de oficina $",
            "costos_energia": "Costos de energía (electricidad, gas, otros) $",
            "servicios_terceros_logistica": "Servicios de terceros en logística (3PL) $",
            "otros_gastos": "Otros gastos $"
        }
        
        # Mapeo para inversiones
        self.inversiones = {
            "inversiones_edificio_terreno": "Inversiones en edificio y terreno $",
            "sistema_manejo_materiales": "Sistema de manejo de materiales (montacargas, elevadores, carretillas, baterías, etc) $",
            "sistemas_almacenamiento": "Sistemas de almacenamiento (Racks, Conveyors, carretillas, etc) $",
            "wms": "WMS (licencias, mantenimiento, etc) $",
            "seguros_inventario": "Seguros del inventario $",
            "otras_inversiones": "Otras inversiones $"
        }


class Inventario:
    def __init__(self):
        # Mapeo para datos
        self.datos = {
            "numero_personas_control_inventario": "Número de personas dedicadas al control de inventario (encargados y planeadores)",
            "metros_cuadrados_oficinas_inventarios": "Metros cuadrados de oficinas inventarios",
            "numero_equipos_oficina_inventarios": "Número de equipos (fax, computadoras, etc)"
        }
        
        # Mapeo para costos y gastos
        self.costos_gastos = {
            "numero_skus": "Stock Keeping Unit",
            "numero_proveedores": "Número de proveedores",
            "costos_mano_obra_control_inventario": "Costos de mano de obra de personas dedicadas al control de inventario $",
            "costos_energia_oficina_inventarios": "Costos de energía de la oficina de inventarios $",
            "suministros_oficina_inventarios": "Suministros de oficina de inventarios $",
            "costos_espacio_oficina_inventarios": "Costos de espacio de oficina de inventarios $",
            "otros_gastos_oficina_inventarios": "Otros gastos de la oficina de inventarios $",
            "inversion_hardware": "Costo del Hardware $",
            "inversion_software_inventarios": "Costo del Software $",
            "inversion_promedio_inventario": "Costo promedio del inventario $",
            "costo_financiero_inversion_inventario": "Costo financiero de la inversión"
        }


class Generales:
    def __init__(self):
        # Mapeo para financieros
        self.financieros = {
            "costo_capital_empresa": "Costo de capital de la empresa %",
            "ventas": "Precio de venta $",
            "ventas_al_costo": "Precio de venta al costo $"
        }
        
        # Mapeo para operativos
        self.operativos = {
            "numero_horas_laborales_anuales_fte": "Número de horas laborales anual FTE"
        }
