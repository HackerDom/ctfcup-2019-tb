#include <stdlib.h>

#include "matrix.h"
#include "random.h"


matrix_t* M_create(matrix_size_t width, matrix_size_t height) {
    matrix_t* matrix;
    matrix_cell_t* cells;

    matrix = (matrix_t*)malloc(sizeof(matrix_t));
    cells = (matrix_cell_t*)calloc(width * height, sizeof(matrix_cell_t));
    
    if (matrix == NULL || cells == NULL)
        exit(M_ERR_CALLOC);

    matrix->width = width;
    matrix->height = height;
    matrix->cells = cells;

    return matrix;
}

matrix_t* M_random(matrix_size_t width, matrix_size_t height) {
    matrix_t* matrix;
    matrix_size_t x, y;

    matrix = M_create(width, height);

    for (x = 0; x < width; ++x) {
        for (y = 0; y < height; ++y) {
            M_set(matrix, x, y, R_next());
        }
    }

    return matrix;
}

matrix_cell_t M_get(matrix_t* matrix, matrix_size_t x, matrix_size_t y) {
    if (matrix == NULL)
        exit(M_ERR_NULL);

    if (x < 0 || x >= matrix->width ||
        y < 0 || y >= matrix->height)
        exit(M_ERR_SIZE);

    return matrix->cells[y * matrix->width + x];
}

void M_set(matrix_t* matrix, matrix_size_t x, matrix_size_t y, matrix_cell_t value) {
    if (matrix == NULL)
        exit(M_ERR_NULL);
    
    if (x < 0 || x >= matrix->width ||
        y < 0 || y >= matrix->height)
        exit(M_ERR_SIZE);

    matrix->cells[y * matrix->width + x] = value;
}

matrix_t* M_sum(matrix_t* left, matrix_t* right) {
    matrix_t* result;
    matrix_size_t x, y;

    if (left == NULL || right == NULL)
        exit(M_ERR_NULL);

    if (left->width != right->width ||
        left->height != right->height)
        exit(M_ERR_SIZE);

    result = M_create(left->width, left->height);

    for (x = 0; x < left->width; ++x) {
        for (y = 0; y < left->height; ++y) {
            M_set(result, x, y, M_get(left, x, y) + M_get(right, x, y));
        }
    }

    return result;
}

matrix_t* M_mul(matrix_t* left, matrix_t* right) {
    matrix_t* result;
    matrix_size_t x, y, z;
    matrix_cell_t sum;

    if (left == NULL || right == NULL)
        exit(M_ERR_NULL);
    
    if (left->height != right->width)
        exit(M_ERR_SIZE);

    result = M_create(left->width, right->height);

    for (x = 0; x < left->width; ++x) {
        for (y = 0; y < right->height; ++y) {
            sum = 0;

            for (z = 0; z < left->height; ++z) {
                sum += M_get(left, x, z) * M_get(right, z, y);
            }
            
            M_set(result, x, y, sum);
        }
    }

    return result;
}
