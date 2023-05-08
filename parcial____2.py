import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

class CSVReader:
#se proporciona una ruta donde mira si hay archivos, si no s eproporciona
#la ruta se asumira que es la ectual
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = input("Por favor, ingrese la ruta del archivo o presione Enter para usar la ruta actual:\n")
        if file_path == "":
            self.file_path = os.getcwd()
        else:
            self.file_path = file_path
            if not os.path.exists(file_path):
                raise ValueError(f"La ruta proporcionada '{file_path}' no existe")

# utiliza el módulo "os" para listar los archivos en la ruta y solicita al 
# usuario que seleccione uno o varios archivos separados por comas. 
# Si el usuario ingresa un índice inválido, se genera un error. Finalmente, 
# la función devuelve una lista de rutas de archivo seleccionadas por el usuario.
    
    def choose_file(self):
        files = os.listdir(self.file_path)
        csv_files = [f for f in files if f.endswith('.csv')]
        if not csv_files:
            raise ValueError("No se encontraron archivos CSV en la ruta especificada")
        print("Archivos CSV encontrados:")
        for i, file in enumerate(csv_files):
            print(f"{i+1}. {file}")
        file_indexes = input("Seleccione los archivos que desea abrir separados por comas: ").split(",")
        selected_files = []
        for index in file_indexes:
            file_index = int(index) - 1
            if file_index < 0 or file_index >= len(csv_files):
                raise ValueError("Índice de archivo inválido")
            selected_files.append(os.path.join(self.file_path, csv_files[file_index]))
        return selected_files
    
# obtiene una lista de rutas de archivos CSV seleccionados por el usuario. 
# Luego utiliza un ciclo for para leer cada archivo CSV y almacenar los datos 
# en una lista llamada list_data

    def read_csv_files(self):
        csv_files = self.choose_file()
        list_data = []
        for csv_file in csv_files:
            data = pd.read_csv(csv_file)
            list_data.append(data)
        merged_data = self.select_columns(list_data)
        return merged_data
    
# Recibe un parámetro data, que es una lista de DataFrames que contienen los datos 
# de los archivos CSV seleccionados. 
# Luego, para cada DataFrame, se imprimen las columnas disponibles y se pide al usuario que 
# seleccione las columnas que desea mostrar en la tabla, 
# separadas por comas. La función devuelve una lista de 
# listas que contiene los nombres de las columnas seleccionadas para cada DataFrame.
    
#dataframe (pandas) que se puede pensar como una tabla en SQL o una hoja de cálculo en Excel
    def get_selected_columns(self, data):
        selected_cols = []
        for i, df in enumerate(data):
            print(f"Tabla {i+1}:")
            print(df)
            print("Columnas disponibles:")
            for j, col in enumerate(df.columns):
                print(f"{j+1}. {col}")
            col_indexes = input("Seleccione las columnas que desea mostrar separadas por comas: ").split(",")
            selected_cols.append([df.columns[int(index)-1] for index in col_indexes])
        return selected_cols

# utiliza la lista de columnas seleccionadas para cada DataFrame para seleccionar 
# solo esas columnas y crear una nueva lista de DataFrames con los datos correspondientes 
# a esas columnas, luego utiliza concat de Pandas para fusionar los DataFrames seleccionados en uno solo

    def select_columns(self, data):
        selected_cols = self.get_selected_columns(data)
        selected_data = []
        for i, cols in enumerate(selected_cols):
            selected_data.append(data[i][cols])
        merged_data = pd.concat(selected_data, axis=1)
        return merged_data

    def fit_linear_regression(self, data):
        selected_cols = self.get_selected_columns([data])
        coefficients = []
        for cols in selected_cols:
            if not all(data[col].apply(lambda x: str(x).isdigit()).all() for col in cols):
                print(f"No se puede hacer regresión lineal a la columna {cols} ya que contiene datos no numéricos")
                continue
            X = data[cols[0]].values.reshape(-1, 1)
            y = data[cols[1]].values.reshape(-1, 1)
            reg = LinearRegression().fit(X, y)
            coefficients.append((cols[0], cols[1], reg.coef_[0][0], reg.intercept_))
        return coefficients
    
    # método para filtrar columnas numéricas
    def filter_numeric_columns(self):
        csv_files = self.choose_file()
        list_data = []
        for csv_file in csv_files:
            data = pd.read_csv(csv_file)
            numeric_cols = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
            list_data.append(data[numeric_cols])
        merged_data = pd.concat(list_data, axis=1)
        return merged_data
    

    def analyze_numeric_columns(self):
        data = self.filter_numeric_columns()
        for col in data.columns:
            print(f"Análisis para la columna '{col}':")
            col_data = data[col]
            # cálculo de estadísticas descriptivas
            mean = col_data.mean()
            std = col_data.std()
            skewness = col_data.skew()
            kurtosis = col_data.kurtosis()
            print(f"Media: {mean:.2f}")
            print(f"Desviación estándar: {std:.2f}")
            print(f"Sesgo: {skewness:.2f}")
            print(f"Curtosis: {kurtosis:.2f}")
            # gráfico Q-Q
            fig, ax = plt.subplots(figsize=(8, 4))
            stats.probplot(col_data, plot=ax)
            ax.set_title(f"Gráfico Q-Q de la columna '{col}'")
            plt.show()
    
csv_reader = CSVReader()
data = csv_reader.read_csv_files()
print("Datos combinados:")
print(data)

coefficients = csv_reader.fit_linear_regression(data)
print("Coeficientes de regresión lineal:")
for coeff in coefficients:
    print(f"{coeff[0]} vs. {coeff[1]}: {coeff[2]}")

# Graficar los valores de la tabla
plt.scatter(data.iloc[:,0], data.iloc[:,1])

for coeff in coefficients:
    x = data[coeff[0]]
    y = data[coeff[1]]
    reg_line = coeff[2]*x + coeff[3] # línea de regresión
    #plt.plot(x, reg_line, label=f"Regresión {coeff[0]} vs {coeff[1]}")
    plt.plot(x, reg_line, color='red', label=f"Regresión {coeff[0]} vs {coeff[1]}")

# Agregar título y leyendas al gráfico
plt.title('Valores de la tabla y regresión lineal')
plt.xlabel('Variable independiente')
plt.ylabel('Variable dependiente')
plt.legend()

# Mostrar el gráfico
plt.savefig("grafica")

csv_reader = CSVReader()

# data = csv_reader.filter_numeric_columns()
# print("Columnas numéricas:")
# print(data.columns)
# print("Estadísticas descriptivas:")
# print(data.describe())
csv_reader.analyze_numeric_columns()


    



































