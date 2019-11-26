#include "source.h"

#define MAP_SIZE 8 * 1024 * 1024

int is_signed = 0;
int is_signed_read = 0;


int main()
{
	setup();

	while ( 1 )
	{
		puts( "---- Teleport ----" );
		auth_menu();

		int option = readInt();

		switch( option )
		{
			case 1:
				login();
				break;
			case 2:
				reg();
				break;
			case 3:
				exit( -1 );
				break;
			default:
				exit( ERROR_OPTION_EXIT );
		}
	}

	return 1;
}

void setup( void )
{
	srand( time( NULL ) );

	setvbuf( stdout, 0, 2, 0 );
	setvbuf( stderr, 0, 2, 0 );
	setvbuf( stdin,  0, 2, 0 );
};

unsigned int readInt()
{
	char* tmpBuf = (char*) malloc( 128 );
	read( 0, tmpBuf, 128 );
	
	unsigned int result = 0xdeadbeef;
	result = (unsigned int) atoi( tmpBuf );

	free( tmpBuf );
	tmpBuf = NULL;

	return result;
};

void teleport_menu( void )
{
	puts( "1. Make teleport" );
	puts( "2. Teleportation" );
	puts( "3. Read sign" );
	puts( "4. Exit" );
	printf( "> " );
};

void auth_menu( void )
{
	puts( "1. Login" );
	puts( "2. Register" );
	puts( "3. Exit" );
	printf( "> " );
};

int login( void )
{
	char InpUsername[ MAX_BUF_SIZE ];
	char InpPassword[ MAX_BUF_SIZE ];

	printf( "{?} login: " );
	int nbytes = read( 0, InpUsername, MAX_BUF_SIZE );

	InpUsername[ nbytes - 1 ] = '\0';

	if ( strcmp( InpUsername, username ) )
	{
		puts( "{-} login error!" );
		return 0;
	}

	printf( "{?} password: " );
	nbytes = read( 0, InpPassword, MAX_BUF_SIZE );
	InpPassword[ nbytes - 1 ] = '\0';
	
	if ( strcmp( InpPassword, password ) )
	{
		puts( "{-} password error!" );
		return 0;
	}

	InpPassword[ nbytes - 1 ] = '\0';

	main_menu(); // bank();

	return 1;
};

int reg( void )
{
	printf( "{?} Enter login: " );
	int nbytes = read( 0, username, MAX_BUF_SIZE );

	username[ nbytes - 1 ] = '\0';

	printf( "{?} Enter password: " );
	nbytes = read( 0, password, MAX_BUF_SIZE ); 
	
	password[ nbytes - 1 ] = '\0';

	return 1;
};

int main_menu( void )
{	
	char teleport_buffer[ 256 ];
	char* teleport = NULL;
	
	int current_teleport_idx = 0;
	int last_teleport_idx = 0;
	
	while( 1 )
	{
		teleport_menu();
		int option = readInt();
			
		int src_x;
		int src_y;
		int src_z;
		
		long long int teleport_time;

		int trash = 0xdeadbeef;

		switch ( option )
		{
			case 1:
			{
				if ( teleport != NULL )
				{
					puts( "{??} You already have a teleport!" );
				}
				else
				{
					teleport = make_teleport();
				}

				break;
			}

			case 2:
				teleportation( 
					&current_teleport_idx,
					&src_x,
					&src_y,
					&src_z,
					&teleport_time,
					trash,
					teleport
				);
				break;
			case 3:
				read_sign( 
					&current_teleport_idx,
					teleport
				);
				break;
			case 4:
				return 0;
			default:
				break;
		}
	}

    return 0;
};

char* make_teleport( void )
{
    char* teleport = mmap( 0, MAP_SIZE, PROT_READ | PROT_WRITE,  MAP_ANON | MAP_PRIVATE, -1, 0 );
    
    if ( teleport == MAP_FAILED )
        return NULL;

    return teleport;
}

int teleportation( 
	int* cur_tel_idx, 
	int *x,
	int *y,
	int *z,
	long long int* t_time,
	int trash,
	char* teleport
)
{
	char tmp_buf[ 256 ];

	if ( teleport == NULL )
	{
		puts( "{-} Teleport is not init!" );
		return 0;
	}

	printf( "{?} Enter teleportation idx: " );

	unsigned int tel_idx = readInt();

	*cur_tel_idx = tel_idx;

	*x = (int)tel_idx / 1000;
	*y = (int)tel_idx / 100;
	*z = (int)tel_idx % 10;

	printf( "{?} Enter data to teleportation: " );

	int nbytes = read( 0, tmp_buf, 512 );
	tmp_buf[ nbytes - 1 ] = '\0';	

	if ( nbytes > 0 )
	{
		memset( teleport, 0, nbytes );
		memcpy( teleport, tmp_buf, nbytes );
	}

	if ( !is_signed )
	{
		printf( "{?} Enter your sign: " );
		nbytes = read( 0, teleport + tel_idx, 9 );

		*( teleport + tel_idx + nbytes - 1 ) = '\0';
		is_signed = 1;
	}

	t_time = time( NULL );
	puts( "{+} You have been teleported!" );
	
	puts( "{?} Do you want teleport in another place?" );
	puts( "1. Yes" );
	puts( "2. No" );
	printf( "> " );

	int option = readInt();

	if ( option == 1 )
	{
		printf( "{?} Enter teleportation idx: " );

		unsigned int tel_idx = readInt();

		*cur_tel_idx = tel_idx;

		*x = (int)tel_idx / 1000;
		*y = (int)tel_idx / 100;
		*z = (int)tel_idx % 10;

		printf( "{?} Enter data to teleportation: " );

		int nbytes = read( 0, tmp_buf, 512 );
		tmp_buf[ nbytes - 1 ] = '\0';	

		if ( nbytes > 0 )
		{
			memset( teleport, 0, nbytes );
			memcpy( teleport, tmp_buf, nbytes );
		}
	}

	return 1;
}

int read_sign( 
	int* cur_tel_idx,
	char* teleport 
)
{
	if ( is_signed )
	{
		if ( is_signed_read )
		{
			puts( "[-] You already read sign!" );
			return 1;
		}

		write( 1, teleport + *cur_tel_idx, 8 );
		puts( "" );
		is_signed_read = 1;
	}
	else
	{
		puts( "[-] Sign is not init!" );
	}

	return 1;
};

int edit_teleport_data(
	char* teleport,
	int teleport_data_size;
)
{
	return 1;
}
