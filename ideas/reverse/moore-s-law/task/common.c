#include <stdio.h>
#include <stdlib.h>

#include "common.h"
#include "random.h"
#include "matrix.h"


int flag_secret[T_FLAGLEN] = {127, 42909, 29628, 17335, 49205, 41212, 45413, 64027, 8313, 14166, 35491, 44347, 63132, 37883, 50076, 1293, 44114, 38684, 31489, 59717, 49715, 15411, 46932, 65366, 24, 54027, 55218, 33324, 43777, 31509, 8301, 45562, 56329, 38975, 22796, 23295, 14886, 2400, 3129, 26370};

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
    matrix_size_t i, j;

    for (i = 0; i < T_FLAGLEN; ++i) {
        for (j = 0; j < matrix->height; j++) {
            flag_secret[i] ^= M_get(matrix, i, j);
        }
        
        putc((char)flag_secret[i], stdout);
    }
}
