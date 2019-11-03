#include <stdio.h>
#include <stdlib.h>

#include "common.h"
#include "random.h"
#include "matrix.h"


int flag_secret[T_FLAGLEN] = {64077, 18475, 39424, 44789, 32247, 63296, 38475, 63825, 61887, 12734, 14477, 40017, 22380, 35409, 15036, 7639, 48674, 37740, 4003, 48671, 54493, 41905, 12736, 37310, 62064, 13737, 20110, 21164, 53155, 50867, 1983, 45410, 62855, 11041, 27592, 1853, 29406, 3344, 58675, 47702};

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    R_seed(1337133713371337ULL, 0x1337133713371337ULL);
}

matrix_size_t get_size() {
    return R_next() % T_MAXSIZE;
}

void fill_sizes(matrix_size_t* sizes, size_t len) {
    size_t i;

    for (i = 0; i < len; ++i) {
        sizes[i] = get_size();
    }
}

void print_flag(matrix_t* matrix) {
    size_t i;

    for (i = 0; i < T_FLAGLEN; ++i) {
        putc((char)(M_get(matrix, i, 0) - flag_secret[i]), stdout);
    }
}
