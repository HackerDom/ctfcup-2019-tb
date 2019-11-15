#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE_DATA 64
#define SIZE_POLY 17
#define SIZE_STATE 16

#define FILENAME_IN "flag.txt"
#define FILENAME_OUT "flag.txt.enc"
#define FILENAME_RANDOM "/dev/urandom"


typedef unsigned int data_t;
typedef unsigned long long data_mul_t;

data_t base = 4294967291;

void encrypt(data_t* data, data_t* poly, data_t* state) {
    size_t i, j;
    data_mul_t temp_value;

    for (i = 0; i < SIZE_DATA; i++) {
        data[i] = (data[i] ^ state[0]) % base;
        temp_value = 0;

        for (j = 0; j < SIZE_STATE; j++) {
            temp_value += ((data_mul_t)poly[j] * (data_mul_t)state[j]) % base;

            if (j > 0) {
                state[j - 1] = state[j];
            }
        }

        state[SIZE_STATE - 1] = temp_value % base;
    }
}

int main(int argc, char** argv, char** envp) {
    FILE* file;

    data_t data[SIZE_DATA];
    data_t poly[SIZE_POLY];
    data_t state[SIZE_STATE];

    memset(data, 0, SIZE_DATA * sizeof(data_t));
    memset(poly, 0, SIZE_POLY * sizeof(data_t));
    memset(state, 0, SIZE_STATE * sizeof(data_t));

    if ((file = fopen(FILENAME_IN, "r")) == NULL) {
        return -1;
    }

    fread(data, sizeof(data_t), SIZE_DATA, file);
    fclose(file);

    if ((file = fopen(FILENAME_RANDOM, "r")) == NULL) {
        return -1;
    }

    fread(poly, sizeof(data_t), SIZE_POLY, file);
    fread(state, sizeof(data_t), SIZE_STATE, file);
    fclose(file);

    encrypt(data, poly, state);

    if ((file = fopen(FILENAME_OUT, "w")) == NULL) {
        return -1;
    }

    fwrite(data, sizeof(data_t), SIZE_DATA, file);
    fclose(file);

    return 0;
}
