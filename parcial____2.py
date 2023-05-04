import os
import pandas as pd

class CSVReader:
    def __init__(self, file_path=None):
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

    def select_columns(self, data):
        for i, df in enumerate(data):
            print(f"Tabla {i+1}:")
            print(df)
            print("Columnas disponibles:")
            for j, col in enumerate(df.columns):
                print(f"{j+1}. {col}")
            col_indexes = input("Seleccione las columnas que desea mostrar separadas por comas: ").split(",")
            selected_cols = [df.columns[int(index)-1] for index in col_indexes]
            selected_data = df[selected_cols]
            data[i] = selected_data
        merged_data = pd.concat(data, axis=1)
        return merged_data

    def read_csv_files(self):
        csv_files = self.choose_file()
        list_data = []
        for csv_file in csv_files:
            data = pd.read_csv(csv_file)
            list_data.append(data)
        merged_data = self.select_columns(list_data)
        return merged_data

csv_reader = CSVReader()
csv_reader.prompt_file_path()  # Preguntar al usuario por la ruta del archivo
data = csv_reader.read_csv_files()
print(data)


