#ifndef _H_MATRIX
#define _H_MATRIX

#include <stdint.h>

#define M_ERR_CALLOC -1
#define M_ERR_NULL -2
#define M_ERR_SIZE -3


typedef uint16_t matrix_cell_t;
typedef uint16_t matrix_size_t;

typedef struct matrix_t {
    matrix_size_t width;
    matrix_size_t height;
    matrix_cell_t* cells;
} matrix_t;


matrix_t* M_create(matrix_size_t width, matrix_size_t height);
matrix_t* M_random(matrix_size_t width, matrix_size_t height);
matrix_cell_t M_get(matrix_t* matrix, matrix_size_t x, matrix_size_t y);
void M_set(matrix_t* matrix, matrix_size_t x, matrix_size_t y, matrix_cell_t value);
matrix_t* M_add(matrix_t* left, matrix_t* right);
matrix_t* M_mul(matrix_t* left, matrix_t* right);


#endif
