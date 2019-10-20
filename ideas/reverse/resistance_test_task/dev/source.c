#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Cup{ea9d371ee29e03cf04054bc1154a8b0b4513614d246fe4653adc7e03f4a2ac65}

#define N 256   // 2^8

unsigned char encrypted_flag[] = {101, 249, 69, 206, 138, 96, 224, 144, 254, 102, 255, 103, 239, 27, 209, 46, 241, 107, 164, 15, 150, 158, 190, 192, 11, 136, 195, 64, 6, 39, 90, 210, 223, 166, 21, 13, 141, 239, 207, 41, 131, 164, 68, 61, 215, 155, 244, 158, 135, 103, 77, 207, 78, 90, 224, 107, 244, 19, 225, 220, 187, 206, 115, 20, 238, 9, 227, 79, 70};

void swap( unsigned char *a, unsigned char *b )
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int KSA( char *key, unsigned char *S ) 
{
    int len = strlen(key);
    int j = 0;

    for(int i = 0; i < N; i++)
        S[i] = i;

    for(int i = 0; i < N; i++) {
        j = (j + S[i] + key[i % len]) % N;

        swap(&S[i], &S[j]);
    }

    return 0;
}

int PRGA( unsigned char *S, char *plaintext, unsigned char *ciphertext )
{
    int i = 0;
    int j = 0;

    for ( size_t n = 0, len = strlen(plaintext); n < len; n++ ) 
    {
        i = ( i + 1 ) % N;
        j = ( j + S[ i ] ) % N;

        swap( &S[ i ], &S[ j ] );
        int rnd = S[ ( S[ i ] + S[ j ] ) % N ];

        ciphertext[ n ] = rnd ^ plaintext[ n ];
    }

    return 0;
}

int RC4( char *key, char *plaintext, unsigned char *ciphertext ) 
{
    unsigned char S[ N ];
    KSA( key, S );

    PRGA( S, plaintext, ciphertext );

    return 0;
}

int main( int argc, char *argv[] ) {

    if ( argc < 2 ) 
    {
        printf( "Usage: %s <password>\n", argv[ 0 ] );
        return -1;
    }

    unsigned char *ciphertext = malloc( sizeof(int) * strlen( argv[ 1 ] ) );

    RC4( "this_is_not_flag", argv[ 1 ], ciphertext);

    if ( !memcmp( ciphertext, encrypted_flag, 69 ) )
    {
    	puts( "[+] Correct flag!" );
    }
    else
    {
    	puts( "[-] Incorrect flag!" );
    }

    return 0;
}