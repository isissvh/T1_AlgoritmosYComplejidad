# Documentación

Se trabajó en dos problemas principales:

- **Ordenamiento de arreglos unidimensionales**
- **Multiplicación de matrices**

Para cada caso se implementaron algoritmos en C++, se generaron datasets mediante scripts, se ejecutaron mediciones de tiempo y memoria, y posteriormente se construyeron gráficos para analizar los resultados.

## Entrega

La entrega se realiza vía **aula.usm.cl** en formato `.zip`.

Dado al tamaño de la entrega, todos los casos de uso se encuentran en mi [repositorio](https://github.com/isissvh/T1_AlgoritmosYComplejidad)

## Multiplicación de matrices

Algoritmos implementados:

- **Naive**
- **Strassen**

### Programa principal

El programa principal de esta sección está implementado en C++ y se encarga de:

- leer matrices de entrada desde archivos
- ejecutar el algoritmo seleccionado
- medir tiempo de ejecución
- medir consumo de memoria
- guardar los resultados de salida y las mediciones correspondientes

### Scripts

Para ejecutar todo (generadores y ejecución) : `make all`

Solo generador de matrices : `make matrix`

Solo ejecución : `make run`

Solo gráficos : `make plots`

## Ordenamiento de arreglo unidimensional

Algoritmos implementados:

- **MergeSort**
- **QuickSort**
- **std::sort**

### Programa principal

El programa principal de esta sección está implementado en C++ y se encarga de:

- leer arreglos de números enteros desde archivos de texto
- ejecutar el algoritmo de ordenamiento seleccionado (MergeSort, QuickSort o std::sort)
- medir el tiempo de ejecución del algoritmo
- medir el consumo máximo de memoria residente (peak RSS)
- guardar el arreglo resultante y exportar las métricas registradas para su análisis

### Scripts

Para ejecutar todo (generadores y ejecución) : `make all`

Solo generador de matrices : `make array`

Solo ejecución : `make run`

Solo gráficos : `make plots`
