import pandas as pd
import os

class ArchivosDatos:

    def __init__(self, *args, **kwargs):
        self.archivos = args
        self.ubicaciones = kwargs
        self.base_datos = pd.DataFrame()

        # Si no se ingresó ningún archivo, se genera una base de datos vacía
        if not self.archivos:
            self.generar_base_datos()

    def generar_base_datos(self):
        # Se genera un DataFrame vacío
        self.base_datos = pd.DataFrame()

    def leer_archivos(self):
        for archivo in self.archivos:
            # Si se ingresó la ubicación del archivo, se usa esa ubicación
            # Si no, se asume que el archivo está en la ubicación actual
            ubicacion = self.ubicaciones.get(archivo, '.')
            ruta_archivo = os.path.join(ubicacion, archivo)

            # Se intenta leer el archivo como CSV o Excel
            try:
                df = pd.read_csv(ruta_archivo)
            except:
                try:
                    df = pd.read_excel(ruta_archivo)
                except:
                    print(f"No se pudo leer el archivo {archivo}")
                    continue

            # Se agrega el contenido del archivo a la base de datos
            self.base_datos = pd.concat([self.base_datos, df])

    def mostrar_base_datos(self):
        print(self.base_datos)

# Ejemplo de uso
archivos = ('sample.csv', 'Weather Test Data.csv')
ubicaciones = {'sample.csv': 'C:/Users/camil/Desktop/parcial2', 'Weather Test Data.csv': 'C:/Users/camil/Desktop/parcial2'}
mi_clase = ArchivosDatos(*archivos, **ubicaciones)
mi_clase.leer_archivos()
mi_clase.mostrar_base_datos()