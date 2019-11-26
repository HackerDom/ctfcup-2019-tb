#include <stdio.h>
#include <limits.h>
#include <stdint.h>
#include <stdlib.h>

#include "matrix.h"
#include "chain.h"
#include "matrixio.h"


void OPT_find_order(matrix_size_t* sizes, size_t n) {
    uint64_t len, i, j, k, temp, cost;

    n--;
    
    OPT_costs = (uint64_t**)malloc(n * sizeof(uint64_t*));
    for (i = 0; i < n; ++i) {
        OPT_costs[i] = (uint64_t*)calloc(n, sizeof(uint64_t));
    }
 
    OPT_order = (uint64_t**)malloc(n * sizeof(uint64_t*));
    for (i = 0; i < n; ++i) {
        OPT_order[i] = (uint64_t*)calloc(n, sizeof(uint64_t));
    }
 
    for (len = 1; len < n; ++len) {
        for (i = 0; i < n - len; ++i) {
            j = i + len;
            OPT_costs[i][j] = LONG_MAX;

            for (k = i; k < j; ++k) {
                temp = (uint64_t)sizes[i] * (uint64_t)sizes[k + 1] * (uint64_t)sizes[j + 1];
                cost = OPT_costs[i][k] + OPT_costs[k + 1][j] + temp;
                
                if (cost < OPT_costs[i][j]) {
                    OPT_costs[i][j] = cost;
                    OPT_order[i][j] = k;
                }
            }
        }
    }
}

uint64_t OPT_mul_order(uint64_t i, uint64_t j) {
    matrix_t* left;
    matrix_t* right;
    matrix_t* result;
    uint64_t left_index, right_index, result_index;
    
    if (i == j)
        return i;
    
    left_index = OPT_mul_order(i, OPT_order[i][j]);
    right_index = OPT_mul_order(OPT_order[i][j] + 1, j);
    result_index = (left_index << 32) + (right_index << 24);

    left = MIO_read_matrix(left_index);
    right = MIO_read_matrix(right_index);
    result = M_mul(left, right);
    
    MIO_write_matrix(result, result_index);
    
    free(left->cells);
    free(left);
    free(right->cells);
    free(right);
    free(result->cells);
    free(result);

    return result_index;
}

void OPT_free(uint64_t n) {
    uint64_t i;

    for (i = 0; i <= n - 2; ++i)  {
        free(OPT_costs[i]);
        free(OPT_order[i]);
    }

    free(OPT_costs);
    free(OPT_order);
}
