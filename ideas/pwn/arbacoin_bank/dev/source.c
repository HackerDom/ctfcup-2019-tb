#include "source.h"

static struct cell* list_of_cells[ 32 ];
static char username[ MAX_BUF_SIZE ];

static int list_idx = 0;
static char password[ MAX_BUF_SIZE ];

int main()
{
	setup();

	while ( 1 )
	{
		puts( "---- Arbacoin Bank ----" );
		auth_menu();

		int option = (int) ReadInt();

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

	return 0;
};

void setup( void )
{
	setvbuf( stdout, 0, 2, 0 );
  	setvbuf( stderr, 0, 2, 0 );
  	setvbuf( stdin,  0, 2, 0 );
};

void auth_menu( void )
{
	puts( "1. Login" );
	puts( "2. Register" );
	puts( "3. Exit" );
	printf( "> " );
};

void basic_menu( void )
{
	puts( "1. Create cell" );
	puts( "2. Delete cell" );
	puts( "3. Edit cell info" );
	puts( "4. Exit" );
	printf( "> " );
};

int login( void )
{
	char InpUsername[ MAX_BUF_SIZE ];
	char InpPassword[ MAX_BUF_SIZE ];

	printf( "login: " );
	int nbytes = read( 0, InpUsername, MAX_BUF_SIZE );

	InpUsername[ nbytes - 1 ] = '\0';

	if ( strcmp( InpUsername, username ) )
	{
		puts( "login error!" );
		return 0;
	}

	printf( "password: " );
	nbytes = read( 0, InpPassword, MAX_BUF_SIZE );
	InpPassword[ nbytes - 1 ] = '\0';
	
	if ( strcmp( InpPassword, password ) )
	{
		puts( "password error!" );
		return 0;
	}

	InpPassword[ nbytes - 1 ] = '\0';

	bank();

	return 1;
};

int reg( void )
{
	printf( "Enter login: " );
	int nbytes = read( 0, username, MAX_BUF_SIZE );

	username[ nbytes - 1 ] = '\0';

	printf( "Enter password: " );
	nbytes = read( 0, password, MAX_BUF_SIZE ); 
	
	password[ nbytes - 1 ] = '\0';

	return 1;
};

int bank( void )
{
	while ( 1 )
	{
		puts( "---- Arbacoin Bank ----" );
		basic_menu();

		int option = (int) ReadInt();

		switch ( option )
		{
			case 1:
				create_cell();
				break;
			case 2:
				delete_cell();
				break;
			case 3:
				change_cell_info();
				break;
			case 4:
			{
				printf( "Goodbye %s\n", username );
				return ERROR_OPTION_EXIT;
			}
		}
	}	
};

int create_cell( void )
{
	struct cell* new_cell = (struct cell*) malloc( sizeof( struct cell ) );

	printf( "Enter balance: " );
	int tmp_balance = (int) ReadInt;

	new_cell->balance = tmp_balance;

	printf( "Enter info: " );
	read( 0, new_cell->info, 120 );

	list_of_cells[ list_idx ] = new_cell;
	printf( "Cell with id [%d] successfully created!\n", list_idx );
	list_idx += 1;

	return 1;
};

int change_cell_info( void )
{
	printf( "Enter sell id (0-31): " );

	unsigned int cell_id = ReadInt();

	printf( "Enter new info: " );
	fflush( stdout );

	int nbytes = read( 0, list_of_cells[ cell_id ]->info, 120 );

	printf( "Info for cell with id [%d] changed!\n", cell_id );

	return 1;
};

int delete_cell( void )
{
	printf( "Enter sell id (0-31): " );

	unsigned int cell_id = ReadInt();

	struct cell* tmp_cell = list_of_cells[ cell_id ];

	free( tmp_cell );

	return 1;
};

unsigned int ReadInt()
{
	char* buf = (char*) malloc( 128 );
	unsigned int value = 0;

	read( 0, buf, 128 );

	if ( buf[ 0 ] == '-' )
		return 0;

	value = atoi( buf );
	free( buf );

	return value;
};
