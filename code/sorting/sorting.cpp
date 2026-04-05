#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm>
#include <ctime>

using namespace std;
using namespace std::chrono;

// =========================================================================
// DECLARACIÓN DE FUNCIONES EXTERNAS
// =========================================================================
void quickSort(vector<int>& arr, int low, int high);
void mergeSort(vector<int>& arr, int left, int right);
vector<int> sortArray(vector<int>& arr);

int main(int argc, char* argv[]) {
    // 1. VERIFICAR ARGUMENTOS DE ENTRADA
    if (argc != 6) {
        cout << "Uso: " << argv[0] << " <algoritmo> <n> <t> <d> <m>\n";
        cout << "Ejemplo: " << argv[0] << " quicksort 1000 ascendente D1 a\n";
        return 1;
    }

    string algoritmo = argv[1];
    string n_str = argv[2];
    int n = stoi(n_str);
    string t = argv[3];
    string d = argv[4];
    string m = argv[5];

    // INICIALIZAR SEMILLA PARA QUICK SORT ALEATORIO
    srand(time(NULL));

    // 2. LEER EL ARCHIVO DE ENTRADA
    string input_filename = "data/array_input/" + n_str + "_" + t + "_" + d + "_" + m + ".txt";
    ifstream infile(input_filename);
    
    if (!infile.is_open()) {
        cerr << "Error: No se pudo abrir el archivo de entrada: " << input_filename << "\n";
        return 1;
    }

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        infile >> arr[i];
    }
    infile.close();

    // 3. MEDIR EL TIEMPO Y EJECUTAR EL ALGORITMO
    auto start_time = high_resolution_clock::now();

    if (algoritmo == "quicksort") {
        quickSort(arr, 0, n - 1);
    } 
    else if (algoritmo == "mergesort") {
        mergeSort(arr, 0, n - 1);
    } 
    else if (algoritmo == "sort") {
        sortArray(arr);
    }
    else {
        cerr << "Error: Algoritmo no reconocido (" << algoritmo << ")\n";
        return 1;
    }

    auto end_time = high_resolution_clock::now();
    duration<double, std::milli> time_span = end_time - start_time;

    // 4. GUARDAR LOS RESULTADOS
    string output_filename = "data/measurements/" + algoritmo + "_results.csv";
    
    ofstream outfile(output_filename, ios::app);
    if (!outfile.is_open()) {
        cerr << "Error: Asegurate de crear la carpeta measurements_sorting/\n";
        return 1;
    }

    outfile << n << "," << t << "," << d << "," << m << "," << time_span.count() << "\n";
    outfile.close();

    cout << "Prueba completada: " << algoritmo << " en " << input_filename 
         << " -> Tiempo: " << time_span.count() << " ms\n";

    return 0;
}