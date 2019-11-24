#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <errno.h>
#include <asm/prctl.h>
#include <sys/prctl.h>
#include <stdint.h>
#include <sys/mman.h>

typedef struct
{
	  int i[4];
} __128bits;


typedef struct
{
	void *tcb;		/* Pointer to the TCB.  Not necessarily the
						   thread descriptor used by libpthread.  */
	void *dtv;
	void *self;		/* Pointer to the thread descriptor.  */
	int multiple_threads;
	int gscope_flag;
	uintptr_t sysinfo;
	uintptr_t stack_guard;
	uintptr_t pointer_guard;
	unsigned long int vgetcpu_cache[2];
	int __glibc_reserved1;
	int __glibc_unused1;
	/* Reservation of some values for the TM ABI.  */
	void *__private_tm[4];
	/* GCC split stack support.  */
	void *__private_ss;
	long int __glibc_reserved2;
	/* Must be kept even if it is no longer used by glibc since programs,
	 *    like AddressSanitizer, depend on the size of tcbhead_t.  */
	__128bits __glibc_unused2[8][4] __attribute__ ((aligned (32)));

	void *__padding[8];
} tcbhead_t;

#define MAX_BUF_SIZE 256
#define MAX_LIST_SIZE 16
#define FAST_CHUNK_SIZE 0x80

#define NORMAL_EXIT 1
#define ERROR_OPTION_EXIT -1
#define MALLOC_ERROR -2 


char username[ MAX_BUF_SIZE ];
char password[ MAX_BUF_SIZE ];

void setup( void );
unsigned int readInt();
void auth_menu( void );
int login( void );
int reg( void );
int teleport( void );
char* make_teleport( void );
int main_menu( void );

int teleportation( 
	int* cur_tel_idx,
	int* x,
	int* y,
	int* z,
	long long int* t_time,
	int trash,
	char* teleport 
);


int read_sign( 
	int* cur_tel_idx,
	char* teleport 
);
