#ifndef _H_RANDOM
#define _H_RANDOM

#include <stdint.h>


typedef struct pcg32_random_t { 
    uint64_t state;
    uint64_t inc; 
} pcg32_random_t;


void R_seed(uint64_t seed, uint64_t inc);
uint32_t R_next();


#endif
