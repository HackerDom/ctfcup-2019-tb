CC=gcc
CFLAGS= -Wall
SECFLAGS=-Wl,-z,noexecstack -fstack-protector-all --pie -fPIE -Wl,-z,relro,-z,now
SOURCE=heap.c
OUTPUT=heap

.PHONY: all clean

all: 
	$(CC) $(CFLAGS) $(SECFLAGS) $(SOURCE) -o $(OUTPUT)

clean:
	rm -rf $(SOURCE)
