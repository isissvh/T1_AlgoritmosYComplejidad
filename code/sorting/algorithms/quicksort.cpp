// // FROM https://www.geeksforgeeks.org/cpp/cpp-program-for-quicksort/ MODIFIED TO USE A RANDOM PIVOT WITHOUT STACK OVERFLOW

// // C++ Program to demonstrate how to implement the quick
// // sort algorithm
#include <bits/stdc++.h>
using namespace std;

int partition(vector<int> &vec, int low, int high) {
    // int mid = low + (high - low) / 2;
    // swap(vec[mid], vec[high]); // con este formato podría mejorarse la ejecución para casos ordenados o casi ordenados.
    int random_index = low + rand() % (high - low + 1);
    swap(vec[random_index], vec[high]);

    int pivot = vec[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        // if (vec[j] <= pivot) { esta versión es más lenta que la de abajo, se generan más intercambios que no son necesarios para casos con muchos elementos iguales
        if (vec[j] < pivot) {
            i++;
            swap(vec[i], vec[j]);
        }
    }

    swap(vec[i + 1], vec[high]);
    return (i + 1);
}

void quickSort(vector<int> &vec, int low, int high) {
    while (low < high) {
        int pi = partition(vec, low, high);

        if (pi - low < high - pi) {
            quickSort(vec, low, pi - 1);
            low = pi + 1;
        } else {
            quickSort(vec, pi + 1, high);
            high = pi - 1;
        }
    }
}

// // int main() {

// //     vector<int> vec = {10, 7, 8, 9, 1, 5};
// //     int n = vec.size();
    
// //     // Calling quicksort for the vector vec
// //     quickSort(vec, 0, n - 1);

// //     for (auto i : vec) {
// //         cout << i << " ";
// //     }
// //     cout << "\n";
    
// //     return 0;
// // }