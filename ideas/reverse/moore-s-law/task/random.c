#include "random.h"


pcg32_random_t rng;

void R_seed(uint64_t seed, uint64_t inc) {
    rng.state = seed;
    rng.inc = inc;
}

uint32_t R_next() {
    uint64_t oldstate = rng.state;
    // Advance internal state
    rng.state = oldstate * 6364136223846793005ULL + (rng.inc|1);
    // Calculate output function (XSH RR), uses old state for max ILP
    uint32_t xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
    uint32_t rot = oldstate >> 59u;
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}
