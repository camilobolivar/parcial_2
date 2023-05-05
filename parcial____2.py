import os
import pandas as pd
from sklearn.linear_model import LinearRegression

class CSVReader:
    def init(self, file_path=None):
        if file_path is None:
            self.file_path = os.getcwd()  # Si no se proporciona una ruta, usar la ruta actual
        else:
            self.file_path = file_path
            if not os.path.exists(file_path):
                raise ValueError(f"La ruta proporcionada '{file_path}' no existe")

    def prompt_file_path(self):
        file_path = input("Por favor, ingrese la ruta del archivo o presione Enter para usar la ruta actual:\n")
        if file_path == "":
            self.file_path = os.getcwd()
        else:
            self.file_path = file_path
            if not os.path.exists(file_path):
                raise ValueError(f"La ruta proporcionada '{file_path}' no existe")

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

    def select_columns(self, data):
        selected_cols = self.get_selected_columns(data)
        selected_data = []
        for i, cols in enumerate(selected_cols):
            selected_data.append(data[i][cols])
        merged_data = pd.concat(selected_data, axis=1)
        return merged_data

    def read_csv_files(self):
        csv_files = self.choose_file()
        list_data = []
        for csv_file in csv_files:
            data = pd.read_csv(csv_file)
            list_data.append(data)
        merged_data = self.select_columns(list_data)
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

csv_reader = CSVReader()
csv_reader.prompt_file_path()
data = csv_reader.read_csv_files()
print("Datos combinados:")
print(data)

coefficients = csv_reader.fit_linear_regression(data)
print("Coeficientes de regresión lineal:")
for coeff in coefficients:
    print(f"{coeff[0]} vs. {coeff[1]}: {coeff[2]}")

import matplotlib.pyplot as plt

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
plt.show()
