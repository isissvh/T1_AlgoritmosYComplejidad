#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// Función naive optimizada para caché (matrices cuadradas n x n)
void matrix_multiplication(int* A, int* B, int* F, int n){
    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < n; k++)
        {
            for (int j = 0; j < n; j++)
            {
                F[i * n + j] += A[i * n + k] * B[k * n + j];
            }
        }
    }
}

int main(int argc, char* argv[]){

    // Guardar los argumentos en variables
    string n_str = argv[1];
    int n = stoi(n_str);
    string t = argv[2];
    string d = argv[3];
    string m_sample = argv[4];

    // Construir los nombres de los archivos
    string base_name = n_str + "_" + t + "_" + d + "_" + m_sample;
    string file1_name = base_name + "_1.txt";
    string file2_name = base_name + "_2.txt";
    string file_out_name = base_name + "_out.txt";

    // Asignación de memoria dinámica para matrices n x n
    int* A = new int[n * n];
    int* B = new int[n * n];
    int* F = new int[n * n](); // Inicializa la matriz F en 0

    // --- LEER MATRIZ A ---
    ifstream file1(file1_name);
    if (!file1.is_open())
    {
        cout << "Error: No se pudo abrir el archivo " << file1_name << "\n";
        return 1;
    }
    for (int i = 0; i < n * n; i++)
    {
        file1 >> A[i];
    }
    file1.close();

    // --- LEER MATRIZ B ---
    ifstream file2(file2_name);
    if (!file2.is_open())
    {
        cout << "Error: No se pudo abrir el archivo " << file2_name << "\n";
        return 1;
    }
    for (int i = 0; i < n * n; i++)
    {
        file2 >> B[i];
    }
    file2.close();

    // --- MULTIPLICAR ---
    matrix_multiplication(A, B, R, n);

    // --- ESCRIBIR MATRIZ RESULTANTE ---
    ofstream file_out(file_out_name);
    if (!file_out.is_open())
    {
        cout << "Error: No se pudo crear el archivo " << file_out_name << "\n";
        return 1;
    }
    
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            file_out << R[i * n + j] << " ";
        }
        file_out << "\n"; // Salto de línea al terminar la fila
    }
    file_out.close();

    // Liberar memoria dinámica
    delete[] A;
    delete[] B;
    delete[] R;

    return 0;
}