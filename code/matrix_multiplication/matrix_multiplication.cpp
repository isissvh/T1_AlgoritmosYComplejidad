#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <filesystem>
#include <sys/resource.h>

using namespace std;
using namespace std::chrono;
namespace fs = std::filesystem;

void naiveMultiply(const vector<long long>& A, const vector<long long>& B, vector<long long>& C, int n);
void strassenMultiply(const vector<long long>& A, const vector<long long>& B, vector<long long>& C, int n);

long getPeakMemoryKB() {
    struct rusage usage;
    if (getrusage(RUSAGE_SELF, &usage) != 0) return -1;
    return usage.ru_maxrss;
}

bool loadMatrix(const string& filename, vector<long long>& M, int n) {
    ifstream infile(filename);
    if (!infile.is_open()) {
        cerr << "Error: No se pudo abrir el archivo de entrada: " << filename << "\n";
        return false;
    }
    M.assign(n * n, 0);
    for (int i = 0; i < n * n; ++i) {
        if (!(infile >> M[i])) {
            cerr << "Error: Formato invalido o faltan datos en " << filename << "\n";
            return false;
        }
    }
    return true;
}

void saveMatrixOutput(const vector<long long>& M, const string& algoritmo, const string& n_str,
                    const string& t, const string& d, const string& m) {
    string output_filename = "data/matrix_output/" + algoritmo + "_" + n_str + "_" + t + "_" + d + "_" + m + ".txt";
    ofstream out(output_filename);
    if (!out.is_open()) {
        cerr << "Error: No se pudo crear el archivo de salida: " << output_filename << "\n";
        return;
    }
    int n = stoi(n_str);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            out << M[i * n + j];
            if (j + 1 < n) out << ' ';
        }
        out << '\n';
    }
}

void saveMeasurement(const string& algoritmo, int n, const string& t, const string& d,
    const string& m, double time_ms, long memory_kb) {
    string csv_filename = "data/measurements/multiplication/" + algoritmo + "_results_rssdelta.csv";
    bool write_header = !fs::exists(csv_filename) || fs::file_size(csv_filename) == 0;
    ofstream outfile(csv_filename, ios::app);
    if (!outfile.is_open()) {
        cerr << "Error: No se pudo abrir el archivo CSV: " << csv_filename << "\n";
        return;
    }
    if (write_header) {
        outfile << "n,t,d,m,time_ms,rss_delta_kb\n";
    }
    outfile << n << ',' << t << ',' << d << ',' << m << ',' << time_ms << ',' << memory_kb << "\n";
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        cout << "Uso: " << argv[0] << " <algoritmo> <n> <t> <d> <m>\n";
        cout << "Ejemplo: " << argv[0] << " naive 1024 aleatorio D1 a\n";
        return 1;
    }

    string algoritmo = argv[1];
    string n_str = argv[2];
    int n = stoi(n_str);
    string t = argv[3];
    string d = argv[4];
    string m = argv[5];

    fs::create_directories("data/matrix_output");
    fs::create_directories("data/measurements");

    string base_name = n_str + "_" + t + "_" + d + "_" + m;
    string input_filename_1 = "data/matrix_input/" + base_name + "_1.txt";
    string input_filename_2 = "data/matrix_input/" + base_name + "_2.txt";

    vector<long long> A, B, C;
    if (!loadMatrix(input_filename_1, A, n)) return 1;
    if (!loadMatrix(input_filename_2, B, n)) return 1;

    long memory_before_kb = getPeakMemoryKB();
    if (memory_before_kb < 0) {
        cerr << "Error al medir memoria antes de ejecutar el algoritmo\n";
        return 1;
    }

    auto start_time = high_resolution_clock::now();
    if (algoritmo == "naive") {
        naiveMultiply(A, B, C, n);
    } else if (algoritmo == "strassen") {
        strassenMultiply(A, B, C, n);
    } else {
        cerr << "Error: Algoritmo no reconocido (" << algoritmo << ")\n";
        return 1;
    }
    auto end_time = high_resolution_clock::now();
    duration<double, milli> time_span = end_time - start_time;

    long memory_after_kb = getPeakMemoryKB();
    if (memory_after_kb < 0) {
        cerr << "Error al medir memoria despues de ejecutar el algoritmo\n";
        return 1;
    }

    long memory_kb = memory_after_kb - memory_before_kb;
    if (memory_kb < 0) memory_kb = 0;

    saveMeasurement(algoritmo, n, t, d, m, time_span.count(), memory_kb);
    saveMatrixOutput(C, algoritmo, n_str, t, d, m);

    cout << "Prueba completada: " << algoritmo
        << " en " << base_name
        << " -> Tiempo: " << time_span.count()
        << " ms, Memoria RSS adicional: " << memory_kb << " KB\n";
    return 0;
}
