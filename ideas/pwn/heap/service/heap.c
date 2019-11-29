#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define CHUNKS_COUNT 16
#define BUFFER_SIZE 1024


void* chunks[CHUNKS_COUNT];


unsigned int get_choice() {
    unsigned int choice;

    puts("[?] Please, select an option:");
    puts("[1] Create chunk.");
    puts("[2] Delete chunk.");
    puts("[3] Print chunk.");
    puts("[4] Exit.");

    scanf("%u", &choice);
    return choice;
}


unsigned int get_index() {
    unsigned int idx;

    puts("[?] Please, input index:");
    scanf("%u", &idx);

    if (idx > CHUNKS_COUNT) {
        puts("[-] Invalid index.");
        return UINT32_MAX;
    }

    if (chunks[idx] == NULL) {
        puts("[-] Chunk is not allocated.");
        return UINT32_MAX;
    }

    return idx;
}


void create_chunk() {
    unsigned int i, size;
    unsigned int idx = CHUNKS_COUNT;
    char buffer[BUFFER_SIZE];

    for (i = 0; i < CHUNKS_COUNT; i++) {
        if (chunks[i] == NULL) {
            idx = i;
            break;
        }
    }

    if (idx == 10) {
        puts("[-] No free chunk slots.");
        return;
    }

    puts("[?] Please, input size:");
    scanf("%u", &size);

    if (size > BUFFER_SIZE - 1) {
        puts("[-] Size is too big.");
        return;
    }

    puts("[?] Please, input data:");
    size = read(0, buffer, size);
    buffer[size] = 0;

    chunks[idx] = (char*)malloc(size);
    strcpy(chunks[idx], buffer);

    puts("[+] Chunk created.");
}


void delete_chunk() {
    unsigned int idx;

    idx = get_index();

    if (idx == UINT32_MAX) {
        return;
    }
    
    free(chunks[idx]);
    chunks[idx] = NULL;

    puts("[+] Successfully deleted chunk.");
}


void print_chunk() {
    unsigned int idx;

    idx = get_index();

    if (idx == UINT32_MAX) {
        return;
    }

    puts(chunks[idx]);
}


void handle() {
    while (1) {
        switch (get_choice()) {
            case 1:
                create_chunk();
                break;
            case 2:
                delete_chunk();
                break;
            case 3:
                print_chunk();
                break;
            case 4:
                return;
            default:
                puts("[-] Invalid choice.");
                break;
        }
    }
}


void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


int main(int argc, char** argv, char** envp) {
    setup();

    handle();
    
    return 0;
}
