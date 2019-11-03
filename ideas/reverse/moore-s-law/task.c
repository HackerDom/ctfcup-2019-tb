#include <stdio.h>
#include <stdlib.h>

#include "common.h"
#include "random.h"
#include "matrix.h"


matrix_t* calculate(matrix_size_t* sizes, size_t len) {
    size_t i;
    matrix_t* left;
    matrix_t* right;
    matrix_t* result;
    
    left = M_random(sizes[0], sizes[1]);

    for (i = 1; i < len - 1; ++i) {
        // printf("%lu\n", i);
        right = M_random(sizes[i], sizes[i + 1]);
        result = M_mul(left, right);
        free(left->cells);
        free(left);
        free(right->cells);
        free(right);
        left = result;
    }

    return result;
}

int main(int argc, char** argv, char** envp) {
    matrix_size_t sizes[T_COUNT];
    matrix_t* result;

    init();
    
    fill_sizes(sizes, T_COUNT);
    result = calculate(sizes, T_COUNT);
    print_flag(result);

    free(result->cells);
    free(result);

    return 0;
}
