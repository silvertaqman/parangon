import pandas as pd
import streamlit as st
import psycopg2
from psycopg2.extras import execute_values
class TransformDF:
    def __init__(self):
        self.expected_columns = [
            "cod_producto",
            "cat_producto",
            "subcat_producto",
            "desc_producto",
            "proveedor",
            "pais",
            "empaque",
            "bultos_tarima",
            "cubicaje_tarima",
            "demanda_mes1",
            "demanda_mes2",
            "demanda_mes3",
            "demanda_mes4",
            "demanda_mes5",
            "demanda_mes6",
            "demanda_mes7",
            "demanda_mes8",
            "demanda_mes9",
            "demanda_mes10",
            "demanda_mes11",
            "demanda_mes12",
            "ordenes_anual",
            "t_entrega_prom",
            "inv_final_bultos",
            "inv_prom_bultos",
            "inv_trans_bultos",
            "precio_uni_bulto",
            "costo_uni_bulto",
            "factor_escazes",
        ]

    # Verifica que el DataFrame contenga todas las columnas esperadas
    def check_df_columns(self, df):
        missing_columns = set(self.expected_columns) - set(df.columns)
        # Encuentra las columnas adicionales que no se esperaban en el DataFrame
        extra_columns = set(df.columns) - set(self.expected_columns)
        # Verifica si el DataFrame contiene exactamente las mismas columnas que se esperaban
        if len(missing_columns) == 0 and len(extra_columns) == 0:
            pass  # si cumple con las columnas se sigue con la ejecución normal
        else:
            # Muestra un mensaje de error si el DataFrame no contiene las mismas columnas que se esperaban
            st.error("El DataFrame no contiene exactamente las mismas columnas.")
            # Comprueba si hay columnas faltantes o columnas adicionales y muestra un mensaje de advertencia
            if len(missing_columns) > 0 or len(extra_columns) > 0:
                warning_message = ""  # Inicializa una cadena de advertencia vacía
                if len(missing_columns) > 0:
                    # Si hay columnas faltantes, agrega un mensaje indicando cuáles son
                    warning_message += f"Columnas faltantes: \n\n{list(missing_columns)}\n\n"
                if len(extra_columns) > 0:
                    # Si hay columnas adicionales, agrega un mensaje indicando cuáles son
                    warning_message += f"Columnas adicionales: \n\n{list(extra_columns)}"
                # Muestra una advertencia en la aplicación Streamlit con el mensaje construido
                st.warning(warning_message)
                # Detiene la ejecución de la aplicación Streamlit si las columnas no coinciden
                st.stop()

            if missing_columns:
                raise ValueError(f"Faltan las siguientes columnas en el archivo: {', '.join(missing_columns)}")
            else:
                st.success('Formato correcto en archivo.')

    # Realiza cálculos para agregar nuevas columnas al DataFrame
    def calculate_df(self, df):
        demanda_cols = [col for col in df.columns if col.startswith("demanda_mes")]
        df['unidades_vendidas'] = df[demanda_cols].sum(axis=1)
        df['bultos_vendidos'] = df['unidades_vendidas'] / df['empaque']
        df['margen_utilidad_ventas'] = (df['precio_uni_bulto'] - df['costo_uni_bulto']) / df['precio_uni_bulto']
        df['ventas_totales'] = df['bultos_vendidos'] * df['precio_uni_bulto']
        df['ventas_al_costo'] = df['bultos_vendidos'] * df['costo_uni_bulto']
        df['margen_bruto'] = df['bultos_vendidos'] * (df['precio_uni_bulto'] - df['costo_uni_bulto'])
        df['valor_inv_prom_bultos'] = df['inv_prom_bultos'] * df['costo_uni_bulto']
        df['rotacion'] = df['ventas_al_costo'] / df['valor_inv_prom_bultos']
        df['meses_inv'] = 12 / df['rotacion']
        df['prom_bultos_desp_mes'] = df[demanda_cols].mean(axis=1)
        df['cubicaje_inv_prom'] = df['cubicaje_tarima'] * (df['inv_final_bultos'] / df['bultos_tarima'])
        return df

    def to_db(self, df, connection_details):
        # Convierte el DataFrame a una lista de diccionarios
        data = df.to_dict('records')
        columns = df.columns.tolist()
        # Prepara los placeholders correctamente
        values_placeholder = ', '.join([f"%({col})s" for col in columns])  # Aquí usamos %(col)s
        # Consulta SQL para insertar datos
        query = f"INSERT INTO stinventario ({', '.join(columns)}) VALUES ({values_placeholder})"

        try:
            with psycopg2.connect(**connection_details) as conn:
                with conn.cursor() as cursor:
                    # Ejecuta el query utilizando execute_values para una inserción eficiente
                    execute_values(cursor, query, data)
                    # Realiza commit de los cambios
                    conn.commit()
                    st.success("Datos subidos a la base de datos correctamente.")
        except Exception as e:
            st.error(f"Error al subir los datos a la base de datos: {e}")

class GeneratedDF:
    def __init__(self):
        self.calculated_columns = [
            "rotacion",
            "valor_inv_prom_bultos",
            "meses_inv",
            "unidades_vendidas",
            "bultos_vendidos",
            "ventas_al_costo",
            "cubicaje_inv_prom",
            "margen_utilidad_ventas",
            "margen_bruto",
            "ventas_totales",
            "prom_bultos_desp_mes",
        ]

    def style_df(self, df, expected_columns):
        # Define los estilos para las celdas
        def highlight_columns(val, column_name):
            if column_name in expected_columns:
                return "background-color: black; color: lawngreen;"
            elif column_name in self.calculated_columns:
                return "background-color: black; color: red;"
            else:
                return ""

        # Aplica estilos condicionales a las celdas en el DataFrame
        def apply_styles(row):
            return [highlight_columns(val, column_name=col) for val, col in zip(row, df.columns)]

        # Aplica los estilos fila por fila usando applymap
        styled_df = df.style.apply(apply_styles, axis=1)

        # Aplica otras configuraciones de estilo
        styled_df = styled_df.set_properties(**{"text-align": "center"})  # Centrado opcional

        # Estilos generales para los encabezados de la tabla
        return styled_df.set_table_styles(
            [{"selector": "th", "props": [("background-color", "gray"), ("color", "white")]}]
        )





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