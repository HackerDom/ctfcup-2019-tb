#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_BUF_SIZE 256

#define NORMAL_EXIT 1
#define ERROR_OPTION_EXIT -1

struct cell
{
	long long int balance;
	char info[ 120 ];
}; // size of struct = 0x80

void setup( void );
void basic_menu( void );
void auth_menu( void );

int bank( void );
int login( void );
int reg( void );

int create_cell( void );
int delete_cell( void );
int change_cell_info( void );
unsigned int ReadInt();