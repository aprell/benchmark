#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// Matrices are N x N
static int N;

static double **A, **B, **C;

static double **malloc_matrix(int nrows, int ncols) {
    double **m = (double **)malloc(nrows * sizeof(double *) +
            nrows * ncols * sizeof(double));

    assert(m);

    // Beginning of first row
    m[0] = (double *)m + nrows;

    for (int i = 1; i < nrows; i++) {
        // Beginning of ith row
        m[i] = m[i-1] + ncols;
    }

    return m;
}

static void multiply(double **A, double **B, double **C) {
    int i, j, k;

    #pragma omp parallel for schedule(static) private(j, k)
    for (i = 0; i < N; i++) {
        for (k = 0; k < N; k++) {
            for (j = 0; j < N; j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char *argv[]) {
    int i, j;

    N = (argc > 1) ? atoi(argv[1]) : 1000;

    A = malloc_matrix(N, N);
    B = malloc_matrix(N, N);
    C = malloc_matrix(N, N);

    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            A[i][j] = i * N + j + 1;
            B[i][j] = (j >= i) ? 1 : 0;
            C[i][j] = 0.0;
        }
    }

    multiply(A, B, C);

    double elapsed = 0;

    for (i = 0; i < 3; i++) {
        double start = omp_get_wtime();
        multiply(A, B, C);
        elapsed += omp_get_wtime() - start;
    }

    elapsed /= 3;

    // "N^3 operations for N^2 data"
    double FLOPS = N * N * N * 2 / elapsed;
    double GFLOPS = FLOPS / 1e9;

    printf("Time: %.2lf s\n", elapsed);
    printf("Performance: %.2lf GFLOPS\n", GFLOPS);

    free(A);
    free(B);
    free(C);

    return 0;
}
