#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm>
#include <ctime>
#include <filesystem>
#include <sys/resource.h>

using namespace std;
using namespace std::chrono;
namespace fs = std::filesystem;

// =========================================================================
// DECLARACIÓN DE FUNCIONES EXTERNAS
// =========================================================================
void quickSort(vector<int>& arr, int low, int high);
void mergeSort(vector<int>& arr, int left, int right);
vector<int> sortArray(vector<int>& arr);

long getPeakMemoryKB() {
    struct rusage usage;
    if (getrusage(RUSAGE_SELF, &usage) != 0) {
        return -1;
    }
    return usage.ru_maxrss;
}

void saveArrayOutput(const vector<int>& arr, const string& algoritmo, const string& n_str, const string& t, const string& d, const string& m) {
    string output_array_filename =
        "data/array_output/" + algoritmo + "_" + n_str + "_" + t + "_" + d + "_" + m + ".txt";

    ofstream out_array(output_array_filename);
    if (!out_array.is_open()) {
        cerr << "Error: No se pudo crear el archivo de salida: "
            << output_array_filename << "\n";
        return;
    }

    for (size_t i = 0; i < arr.size(); i++) {
        out_array << arr[i];
        if (i + 1 < arr.size()) out_array << " ";
    }
    out_array << "\n";
    out_array.close();
}

void saveMeasurement(const string& algoritmo, int n, const string& t, const string& d, const string& m, double time_ms, long memory_kb) {
    // string csv_filename = "data/measurements/" + algoritmo + "_results.csv";
    string csv_filename = "data/measurements/" + algoritmo + "_results_rssdelta.csv";

    bool write_header = !fs::exists(csv_filename) || fs::file_size(csv_filename) == 0;

    ofstream outfile(csv_filename, ios::app);
    if (!outfile.is_open()) {
        cerr << "Error: No se pudo abrir el archivo CSV: " << csv_filename << "\n";
        return;
    }

    if (write_header) {
        // outfile << "n,t,d,m,time_ms,memory_kb\n";
        outfile << "n,t,d,m,time_ms,rss_delta_kb\n";
    }

    outfile << n << ","
            << t << ","
            << d << ","
            << m << ","
            << time_ms << ","
            << memory_kb << "\n";

    outfile.close();
}

int main(int argc, char* argv[]) {

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

    srand(time(NULL));

    fs::create_directories("data/measurements");
    fs::create_directories("data/array_output");

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

    long memory_before_kb = getPeakMemoryKB();
    if (memory_before_kb < 0) {
        cerr << "Error al medir memoria antes de ejecutar el algoritmo\n";
        return 1;
    }

    auto start_time = high_resolution_clock::now();

    if (algoritmo == "quicksort") {
        quickSort(arr, 0, n - 1);
    }
    else if (algoritmo == "mergesort") {
        mergeSort(arr, 0, n - 1);
    }
    else if (algoritmo == "sort") {
        arr = sortArray(arr);
    }
    else {
        cerr << "Error: Algoritmo no reconocido (" << algoritmo << ")\n";
        return 1;
    }

    auto end_time = high_resolution_clock::now();
    duration<double, std::milli> time_span = end_time - start_time;

    long memory_after_kb = getPeakMemoryKB();
    if (memory_after_kb < 0) {
        cerr << "Error al medir memoria despues de ejecutar el algoritmo\n";
        return 1;
    }
    long memory_kb = memory_after_kb - memory_before_kb;
    if (memory_kb < 0) memory_kb = 0;

    saveMeasurement(algoritmo, n, t, d, m, time_span.count(), memory_kb);
    saveArrayOutput(arr, algoritmo, n_str, t, d, m);

    cout << "Prueba completada: " << algoritmo
        << " en " << input_filename
        << " -> Tiempo: " << time_span.count()
        << " ms, Memoria RSS adicional: " << memory_kb << " KB\n";

    return 0;
}