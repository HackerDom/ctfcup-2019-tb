CC=gcc
CFLAGS=-fno-stack-protector
SOURCES=oldschool.c
OUTPUT=oldschool

.PHONY: all clean

all:
	$(CC) $(CFLAGS) $(SOURCES) -o $(OUTPUT)

clean:
	rm -f $(OUTPUT)
