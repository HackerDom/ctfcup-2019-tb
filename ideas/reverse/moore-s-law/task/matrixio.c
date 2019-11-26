#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "matrix.h"
#include "matrixio.h"


void MIO_init() {
    system("rm -rf " MIO_DIRNAME " && mkdir " MIO_DIRNAME);
}

void MIO_write_matrix(matrix_t* matrix, size_t index) {
    FILE* file;
    char path[MIO_PATHLEN];

    sprintf(path, MIO_DIRNAME "/%lu.mtx", index);
    
    if ((file = fopen(path, "wb")) == NULL)
        exit(MIO_ERR_OPEN);

    fwrite(&matrix->width, sizeof(matrix_size_t), 1, file);
    fwrite(&matrix->height, sizeof(matrix_size_t), 1, file);
    fwrite(matrix->cells, sizeof(matrix_cell_t), matrix->width * matrix->height, file);

    fclose(file);
}

matrix_t* MIO_read_matrix(size_t index) {
    FILE* file;
    char path[MIO_PATHLEN];
    matrix_size_t width, height;
    matrix_t* matrix;

    sprintf(path, MIO_DIRNAME "/%lu.mtx", index);
    
    if ((file = fopen(path, "r")) == NULL)
        exit(MIO_ERR_OPEN);
    
    fread(&width, sizeof(matrix_size_t), 1, file);
    fread(&height, sizeof(matrix_size_t), 1, file);

    matrix = M_create(width, height);

    fread(matrix->cells, sizeof(matrix_cell_t), matrix->width * matrix->height, file);

    fclose(file);

    return matrix;
}
