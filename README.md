#mi clase
 reune librerias como os, pandas, sklearn.linear_model,matplotlib.pyplot,matplotlib.pyplot y scipy.stats. 
#init
al iniciar cree un metodo donde el ususrio puede proporcionar una ruta del computador o de lo contrario puede presionar "enter" acogiendo el programa la ruta actual.
#choose_file
utiliza "os" para listar los archivos en la ruta y solicita al usuario que seleccione uno o varios archivos separados por comas. Si el usuario ingresa un índice inválido, se genera un error. Finalmente, la función devuelve una lista de rutas de archivo seleccionadas por el usuario.
#read_csv_files
obtiene una lista de rutas de archivos CSV seleccionados por el usuario. Luego utiliza un ciclo for para leer cada archivo CSV y almacenar los datos para ser retornados como una lisla
#get_selected_columns
Recibe un parámetro data, que es una lista de DataFrames que contienen los datos de los archivos CSV seleccionados. Luego, para cada DataFrame, se imprimen las columnas disponibles y se pide al usuario que seleccione las columnas que desea mostrar en la tabla, separadas por comas. La función devuelve una lista de listas que contiene los nombres de las columnas seleccionadas para cada DataFrame.
#select_columns
utiliza la lista de columnas seleccionadas para cada DataFrame para seleccionar solo esas columnas y crear una nueva lista de DataFrames con los datos correspondientes a esas columnas, luego utiliza concat de Pandas para fusionar los DataFrames seleccionados en uno solo.
#fit_linear_regression
utiliza un método llamado "get_selected_columns" para seleccionar las columnas en las que se realizará la regresión lineal, el método comprueba si todas las columnas seleccionadas contienen datos numéricos, dara una regresion lineal. Si alguna columna contiene datos no numéricos. Guarda los coeficientes de regresión obtenidos para cada par de variables en una lista de coeficientes, si alguna columna tiene un dato tipo cadena el método imprimirá un mensaje de advertencia y omitirá esa columna.
#filter_numeric_columns
llama al metodo "choose_file" para pedir la lista de lista la cual sera fitrada, dejando una lista de todas las columnas numericas.
analyze_numeric_columns
apartir de filtar los archivos y tener la comunas numericas, este metodo calcula la Gausianidad, curtosis y sesgo de cada columna numérica y le da una gráfica Q-Q 
show_columns_with_conditio
El método toma un argumento de datos y solicita al usuario que ingrese la condición que desea buscar en las columnas. Luego, el método itera sobre cada columna en los datos y comprueba si la columna es de tipo objeto (cadena) y si la condición aparece en algún lugar de los valores de la columna. Si la columna cumple ambas condiciones, se agrega a una lista de columnas seleccionadas. Si no se encuentra ninguna columna que contenga la condición, se imprime un mensaje que indica que no se encontraron columnas. De lo contrario, el método imprime un mensaje que indica las columnas seleccionadas que contienen la condición.
