#include <stdio.h>
#include <stdlib.h>

int main()
{
	char Username_first = 'a';
	char Password_first = 'K';

	unsigned long seed = time( NULL ) + (int) Username_first + (int) Password_first;
	seed += 8 + 32; // username len = 8, password len = 32
	seed ^= 0xdeadbeef;

	srand( seed );

	int OTPcode = rand() & 0xffffff;

	printf( "%d", OTPcode );

	return OTPcode;
}