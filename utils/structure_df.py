# structure_df.py
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