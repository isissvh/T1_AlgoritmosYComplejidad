// FROM https://www.geeksforgeeks.org/dsa/strassens-matrix-multiplication/ con pequeñas modificaciones para mejorar el rendimiento

#include <vector>
using namespace std;

static int nextPowerOfTwo(int n) {
    if (n <= 1) return 1;
    int power = 1;
    while (power < n) power <<= 1;
    return power;
}

static vector<vector<long long>> resizeMatrix(const vector<vector<long long>>& mat, int newR, int newC) {
    vector<vector<long long>> resized(newR, vector<long long>(newC, 0));
    for (int i = 0; i < static_cast<int>(mat.size()); ++i) {
        for (int j = 0; j < static_cast<int>(mat[0].size()); ++j) {
            resized[i][j] = mat[i][j];
        }
    }
    return resized;
}

static vector<vector<long long>> add(const vector<vector<long long>>& a,
                                    const vector<vector<long long>>& b,
                                    int size,
                                    int sign = 1) {
    vector<vector<long long>> res(size, vector<long long>(size, 0));
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            res[i][j] = a[i][j] + sign * b[i][j];
        }
    }
    return res;
}

static vector<vector<long long>> strassen(const vector<vector<long long>>& mat1,
                                        const vector<vector<long long>>& mat2) {
    int n = static_cast<int>(mat1.size());
    vector<vector<long long>> res(n, vector<long long>(n, 0));
    if (n == 1) {
        res[0][0] = mat1[0][0] * mat2[0][0];
        return res;
    }

    int newSize = n / 2;
    vector<vector<long long>> a11(newSize, vector<long long>(newSize));
    vector<vector<long long>> a12(newSize, vector<long long>(newSize));
    vector<vector<long long>> a21(newSize, vector<long long>(newSize));
    vector<vector<long long>> a22(newSize, vector<long long>(newSize));
    vector<vector<long long>> b11(newSize, vector<long long>(newSize));
    vector<vector<long long>> b12(newSize, vector<long long>(newSize));
    vector<vector<long long>> b21(newSize, vector<long long>(newSize));
    vector<vector<long long>> b22(newSize, vector<long long>(newSize));

    for (int i = 0; i < newSize; ++i) {
        for (int j = 0; j < newSize; ++j) {
            a11[i][j] = mat1[i][j];
            a12[i][j] = mat1[i][j + newSize];
            a21[i][j] = mat1[i + newSize][j];
            a22[i][j] = mat1[i + newSize][j + newSize];
            b11[i][j] = mat2[i][j];
            b12[i][j] = mat2[i][j + newSize];
            b21[i][j] = mat2[i + newSize][j];
            b22[i][j] = mat2[i + newSize][j + newSize];
        }
    }

    auto m1 = strassen(add(a11, a22, newSize), add(b11, b22, newSize));
    auto m2 = strassen(add(a21, a22, newSize), b11);
    auto m3 = strassen(a11, add(b12, b22, newSize, -1));
    auto m4 = strassen(a22, add(b21, b11, newSize, -1));
    auto m5 = strassen(add(a11, a12, newSize), b22);
    auto m6 = strassen(add(a21, a11, newSize, -1), add(b11, b12, newSize));
    auto m7 = strassen(add(a12, a22, newSize, -1), add(b21, b22, newSize));

    auto c11 = add(add(m1, m4, newSize), add(m7, m5, newSize, -1), newSize);
    auto c12 = add(m3, m5, newSize);
    auto c21 = add(m2, m4, newSize);
    auto c22 = add(add(m1, m3, newSize), add(m6, m2, newSize, -1), newSize);

    for (int i = 0; i < newSize; ++i) {
        for (int j = 0; j < newSize; ++j) {
            res[i][j] = c11[i][j];
            res[i][j + newSize] = c12[i][j];
            res[i + newSize][j] = c21[i][j];
            res[i + newSize][j + newSize] = c22[i][j];
        }
    }
    return res;
}

void strassenMultiply(const vector<long long>& A, const vector<long long>& B, vector<long long>& C, int n) {
    int size = nextPowerOfTwo(n);
    vector<vector<long long>> mat1(n, vector<long long>(n));
    vector<vector<long long>> mat2(n, vector<long long>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            mat1[i][j] = A[i * n + j];
            mat2[i][j] = B[i * n + j];
        }
    }
    vector<vector<long long>> aPad = resizeMatrix(mat1, size, size);
    vector<vector<long long>> bPad = resizeMatrix(mat2, size, size);
    vector<vector<long long>> cPad = strassen(aPad, bPad);
    C.assign(n * n, 0);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i * n + j] = cPad[i][j];
        }
    }
}
