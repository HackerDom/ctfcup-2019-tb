#ifndef _H_CHAIN
#define _H_CHAIN

#include <stdint.h>

#include "matrix.h"


uint64_t **OPT_costs;
uint64_t **OPT_order;

void OPT_find_order(matrix_size_t* sizes, size_t n);
uint64_t OPT_mul_order(uint64_t i, uint64_t j);
void OPT_free(uint64_t n);


#endif
