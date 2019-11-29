#include <stdio.h>
#include <limits.h>
#include <stdint.h>
#include <stdlib.h>

#include "chain.h"
#include "common.h"
#include "random.h"
#include "matrix.h"
#include "matrixio.h"


uint64_t naive_cost(matrix_size_t* sizes, size_t len) {
    size_t i;
    uint64_t naive;

    naive = 0;
    for (i = 0; i < len - 2; i++)
        naive += (uint64_t)sizes[i] * (uint64_t)sizes[i + 1] * (uint64_t)sizes[i + 2];

    return naive;
}

void generate_matrices(matrix_size_t* sizes, size_t len) {
    size_t i;
    matrix_t* matrix;

    for (i = 0; i < len - 1; ++i) {
        matrix = M_random(sizes[i], sizes[i + 1]);
        MIO_write_matrix(matrix, i);
        free(matrix->cells);
        free(matrix);
    }
}

int main() {
    matrix_size_t sizes[T_COUNT];
    matrix_t* matrix;
    uint64_t result_index;

    init();
    MIO_init();
    
    fill_sizes(sizes, T_COUNT);

    printf("Naive cost:\t%lu\n", naive_cost(sizes, T_COUNT));   
    OPT_find_order(sizes, T_COUNT);
    printf("Optimal cost:\t%lu\n", OPT_costs[0][T_COUNT - 2]);

    generate_matrices(sizes, T_COUNT);

    result_index = OPT_mul_order(0, T_COUNT - 2);
    matrix = MIO_read_matrix(result_index);
    print_flag(matrix);

    OPT_free(T_COUNT);
    free(matrix->cells);
    free(matrix);

    return 0;
}
