#include <vector>
using namespace std;
void naiveMultiply(const vector<long long>& A, const vector<long long>& B, vector<long long>& C, int n) {
    C.assign(n * n, 0);
    for (int i = 0; i < n; ++i) {
        const long long* Ai = &A[i * n];
        long long* Ci = &C[i * n];
        for (int k = 0; k < n; ++k) {
            long long aik = Ai[k];
            const long long* Bk = &B[k * n];
            for (int j = 0; j < n; ++j) {
                Ci[j] += aik * Bk[j];
            }
        }
    }
}
