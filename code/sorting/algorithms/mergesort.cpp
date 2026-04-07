// FROM https://www.geeksforgeeks.org/dsa/merge-sort/ MODIFIED TO PRE-ALLOCATE MEMORY PARA MEJORAR RENDIMIENTO

#include <iostream>
#include <vector>

using namespace std;

/* Esta es la versión original, la cual se modificó para mejorar el rendimiento
void merge(vector<int>& arr, int left, int mid, int right){

    int n1 = mid - left + 1;
    int n2 = right - mid;

    // Create temp vectors
    vector<int> L(n1), R(n2);

    // Copy data to temp vectors L[] and R[]
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    int i = 0, j = 0;
    int k = left;

    // Merge the temp vectors back 
    // into arr[left..right]
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of L[], 
    // if there are any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of R[], 
    // if there are any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}
*/

void merge(vector<int>& arr, vector<int>& temp, int left, int mid, int right) {
    int i = left;      
    int j = mid + 1;
    int k = left;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }

    while (i <= mid) {
        temp[k++] = arr[i++];
    }

    while (j <= right) {
        temp[k++] = arr[j++];
    }

    for (i = left; i <= right; i++) {
        arr[i] = temp[i];
    }
}

void mergeSortHelper(vector<int>& arr, vector<int>& temp, int left, int right) {
    if (left >= right) {
        return;
    }

    int mid = left + (right - left) / 2;
    
    mergeSortHelper(arr, temp, left, mid);
    mergeSortHelper(arr, temp, mid + 1, right);
    
    merge(arr, temp, left, mid, right);
}


void mergeSort(vector<int>& arr, int left, int right) {

    vector<int> temp(arr.size());
    
    mergeSortHelper(arr, temp, left, right);
}