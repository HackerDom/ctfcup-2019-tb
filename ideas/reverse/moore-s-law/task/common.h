#ifndef _H_COMMON
#define _H_COMMON

#include "matrix.h"

#define T_COUNT 1024
#define T_MAXSIZE 4096
#define T_FLAGLEN 40


int flag_secret[T_FLAGLEN];

void init();

matrix_size_t get_size();
void fill_sizes(matrix_size_t* sizes, size_t len);

void print_flag(matrix_t* matrix);


#endif
