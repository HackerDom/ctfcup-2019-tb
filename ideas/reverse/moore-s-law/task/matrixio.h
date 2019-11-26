#ifndef _H_MATRIXIO
#define _H_MATRIXIO

#include "matrix.h"

#define MIO_PATHLEN 64
#define MIO_DIRNAME "matrices"

#define MIO_ERR_OPEN 1


void MIO_init();
void MIO_write_matrix(matrix_t* matrix, size_t index);
matrix_t* MIO_read_matrix(size_t index);


#endif
