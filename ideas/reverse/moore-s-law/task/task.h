#ifndef _H_TASK
#define _H_TASK

#include "matrix.h"

#define T_COUNT 1024
#define T_MAXSIZE 4096
#define T_FLAGLEN 40


int secret[T_FLAGLEN] = {64077, 18475, 39424, 44789, 32247, 63296, 38475, 63825, 61887, 12734, 14477, 40017, 22380, 35409, 15036, 7639, 48674, 37740, 4003, 48671, 54493, 41905, 12736, 37310, 62064, 13737, 20110, 21164, 53155, 50867, 1983, 45410, 62855, 11041, 27592, 1853, 29406, 3344, 58675, 47702};

void init();

matrix_size_t get_size();
void fill_sizes(matrix_size_t* sizes, size_t len);

void print_flag(matrix_t* matrix);


#endif
