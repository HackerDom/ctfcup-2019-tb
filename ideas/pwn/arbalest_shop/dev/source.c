#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/mman.h>

#define MAX_BUF_SIZE 256
#define MAX_LIST_SIZE 16
#define FAST_CHUNK_SIZE 0x80

#define NORMAL_EXIT 1
#define ERROR_OPTION_EXIT -1
#define MALLOC_ERROR -2 

enum STATUS { FOR_SALE, SOLD_OUT };


void setup( void );
void basic_menu( void );
void auth_menu( void );

int login( void );
int reg( void );

int shop( void );

int buy_arbalest( void );
int sell_arbalest( void );
int change_arbalest_price( void );
int change_user_password( void );
int change_arbalest_status( void );
void delete_solded_arbalests( void );
int delete_arbalest( int id );

int view_all( void );
int view_arbalest( int );
void view_profile_info( void );
int insert_in_list( char*, int, char*, int );

void* safe_malloc( int );
void safe_free( void*, int );
//void readPrivateToken( void );
int readInt();

void dl_make_heap_executable( void );


struct arbalest 
{
	char* name; // + 0
	long long price; // + 8
	char* owner; // + 16
	long long status; // + 24
};

struct User 
{
	char username[ MAX_BUF_SIZE ];
	char password[ MAX_BUF_SIZE ];
	long long balance;
};


struct User g_User;

int g_list_index = 0;
struct arbalest ArbalestList[ MAX_LIST_SIZE ];

int main()
{
	setup();
	//dl_make_heap_executable();

	while ( 1 )
	{
		puts( "---- Arbalest Shop ----" );
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
};

void setup( void )
{
	srand( time( NULL ) );

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
	puts( "1. Change password" );
	puts( "2. Buy arbalest" );
	puts( "3. Sell arbalest" );
	puts( "4. Change arbalest price" );
	puts( "5. View all arbalest" );
	puts( "6. Change arbalest status");
	puts( "7. View profile info" );
	puts( "8. Delete solded arbalests" );
	puts( "9. Exit" );
	printf( "> " );
};

int login( void )
{
	char InpUsername[ MAX_BUF_SIZE ];
	char InpPassword[ MAX_BUF_SIZE ];

	printf( "[?] Enter login: " );
	int nbytes = read( 0, InpUsername, MAX_BUF_SIZE );

	InpUsername[ nbytes - 1 ] = '\0';

	if ( strcmp( InpUsername, g_User.username ) )
	{
		puts( "[-] Login error!" );
		return 0;
	}

	printf( "[?] Enter password: " );
	nbytes = read( 0, InpPassword, MAX_BUF_SIZE );

	InpPassword[ nbytes - 1 ] = '\0';

	if ( strcmp( InpPassword, g_User.password ) )
	{
		puts( "[-] Password error!" );
		return 0;
	}

	shop();

	return 1;
};

int reg( void )
{
	printf( "[?] Enter login: " );

	int nbytes = read( 0, g_User.username, MAX_BUF_SIZE );
	g_User.username[ nbytes - 1 ] = '\0';

	printf( "[?] Enter password: " );

	nbytes = read( 0, g_User.password, MAX_BUF_SIZE );
	g_User.password[ nbytes - 1 ] = '\0';

	g_User.balance = 100;

	return 1;
};

int shop( void )
{
	while ( 1 )
	{
		puts( "---- Arbalest Shop ----" );
		basic_menu();

		int option = readInt();

		switch ( option )
		{
			case 1:
				change_user_password();
				break;
			case 2:
				buy_arbalest();
				break;
			case 3:
				sell_arbalest();
				break;
			case 4:
				change_arbalest_price();
				break;
			case 5:
				view_all();
				break;
			case 6:
				change_arbalest_status();
				break;
			case 7:
				view_profile_info();
				break;
			case 8:
				delete_solded_arbalests();
				break;
			case 9:
			{
				printf( "Goodbye %s!\n", g_User.username );
				return ERROR_OPTION_EXIT;
			}
		}
	}	
};

int buy_arbalest( void )
{
	printf( "[?] Enter the arbalest id: " );
	int id = readInt();

	if ( id == 0xdeadbeef )
	{
		printf( "[-] readInt() error!" );
		exit( id ); 
	}

	if ( id < g_list_index )
	{
		if ( !strcmp( ArbalestList[ id ].owner, g_User.username ) )
		{
			puts( "[-] You are the owner of this arbalest" );
			return 0;
		}
		else
		{
			if ( g_User.balance < ArbalestList[ id ].price )
			{
				puts( "[-] Not enough money!" ); // translate ??
			}
			else
			{
				g_User.balance -= ArbalestList[ id ].price;
				ArbalestList[ id ].status = SOLD_OUT;

				safe_free( ArbalestList[ id ].owner, 
					strlen( ArbalestList[ id ].owner ) );

				ArbalestList[ id ].owner = NULL;

				char *arbalest_owner = (char*) safe_malloc( strlen( g_User.username ) );
				strncpy( arbalest_owner, g_User.username, strlen( g_User.username ) );
				printf( "[+] Arbalest owner <%s> is successfully setted!\n", 
					arbalest_owner );

				ArbalestList[ id ].owner = arbalest_owner;

				puts( "[+] Arbalest is successfully buyed!" ); // translate ??
			}
		}
	}
	else
	{
		puts( "[-] Index error!" );
		return 0;
	}

	return 1;
};

int sell_arbalest( void )
{	
	// get name size
	printf( "[?] Enter arbalest name size: " );
	int name_size = readInt();

	if ( name_size == 0xdeadbeef || name_size <= 0 || name_size > 0xffff )
	{
		puts( "[-] Error in name size read!" );
		puts( "[-] Set default name size: 128 byte" );
		name_size = 128;
	}

	// get name
	printf( "[?] Enter arbalest name: " );

	char* arbalest_name = (char*) safe_malloc( name_size + 1 );
	int nbytes = read( 0, arbalest_name, name_size + 1 );

	if ( nbytes <= 0 )
	{
		puts( "[-] Error in arbalest name read" );

		char* randomString = (char*) safe_malloc( FAST_CHUNK_SIZE );
		snprintf( randomString, sizeof( randomString ), "%d", random() );

		strcpy( arbalest_name, g_User.username );
		strcat( arbalest_name, "_" );
		strcat( arbalest_name, randomString );

		printf( "[-] Set default name: %s", arbalest_name );
		
		safe_free( randomString, FAST_CHUNK_SIZE );
		randomString = NULL;
	}
	else
	{
		arbalest_name[ nbytes - 1 ] = '\0';
		printf( "[+] Arbalest name <%s> is successfully setted!\n", 
			arbalest_name );
	}

	// get price
	printf( "[?] Enter arbalest price: " );
	int arbalest_price = 100;

	arbalest_price = readInt();

	if ( arbalest_price <= 0 )
	{
		puts( "[-] Error in arbalest price!" );
		puts( "[-] Set default price: 100 arbc" );
		arbalest_price = 100;
	}
	else
	{
		printf( "[+] Arbalest price <%d> is successfully setted!\n", 
			arbalest_price );
	}

	// set owner
	char *arbalest_owner = (char*) safe_malloc( strlen( g_User.username ) );
	strncpy( arbalest_owner, g_User.username, strlen( g_User.username ) );
	printf( "[+] Arbalest owner <%s> is successfully setted!\n", 
		arbalest_owner );

	// set status
	int arbalest_status = FOR_SALE;

	int result = insert_in_list( arbalest_name, arbalest_price, 
		arbalest_owner, arbalest_status );

	if ( result )
	{
		printf( "[+] Arbalest successfully added in list!\n" );
	}

	return 1;
};

void view_profile_info( void )
{
	puts( "++++++++ Profile ++++++++" );
	
	printf( "Username: %s\n", g_User.username );
	printf( "Password: %s\n", g_User.password );
	printf( "Balance: %d\n", g_User.balance );

	puts( "+++++++++++++++++++++++++" );
};

int view_all( void )
{
	for ( int i = 0; i < g_list_index; i++ )
	{
		view_arbalest( i );
	}

	return 1;
};

int view_arbalest( int id )
{
	if ( g_list_index <= id )
	{
		puts( "[-] Index error" );
		return 0;
	}

	printf( "+++++ Arbalest [%d] +++++\n", id );
	printf( "Name: %s\n", ArbalestList[ id ].name );
	printf( "Prcie: %d\n", ArbalestList[ id ].price );
	printf( "Owner: %s\n", ArbalestList[ id ].owner );

	if ( ArbalestList[ id ].status == FOR_SALE )
	{
		puts( "Status: for sale" );
	}
	else
	{
		puts( "Status: sold out" );
	}

	puts( "+++++++++++++++++++++++++" );

	return 1;
};

int change_arbalest_price( void )
{
	printf( "[?] Enter the arbalest id: " );
	int id = readInt();

	if ( id == 0xdeadbeef )
	{
		printf( "[-] readInt() error!" );
		exit( id ); 
	}

	if ( id < g_list_index )
	{
		if ( strcmp( ArbalestList[ id ].owner, g_User.username ) )
		{
			puts( "[-] You are not the owner of this arbalest" );
			return 0;
		}
		else
		{
			printf( "[?] Enter new arbalest price: " );
			int new_price = readInt();

			if ( new_price == 0xdeadbeef )
			{
				printf( "[-] readInt() error!" );
				exit( new_price );
			}

			ArbalestList[ id ].price = new_price;
		}
	}
	else
	{
		puts( "[-] Index error!" );
		return 0;
	}

	return 1;
};

int change_arbalest_status( void )
{
	printf( "[?] Enter the arbalest id: " );
	int id = readInt();

	if ( id == 0xdeadbeef )
	{
		printf( "[-] readInt() error!" );
		exit( id ); 
	}

	if ( id < g_list_index )
	{
		if ( strcmp( ArbalestList[ id ].owner, g_User.username ) )
		{
			puts( "[-] You are not the owner of this arbalest" );
			return 0;
		}
		else
		{
			puts( "[?] 0 - for sale, 1 - sold out" );
			printf( "[?] Enter new arbalest status: " );
			
			int new_status = readInt();

			if ( new_status == 0xdeadbeef )
			{
				printf( "[-] readInt() error!" );
				exit( new_status );
			}

			if ( new_status == FOR_SALE )
			{
				ArbalestList[ id ].status = FOR_SALE;
			}
			else if ( new_status == SOLD_OUT )
			{
				ArbalestList[ id ].status = SOLD_OUT;
			}
			else
			{
				puts( "[-] Error status value!" );
				return 0;
			}
		}
	}
	else
	{
		puts( "[-] Index error!" );
		return 0;
	}

	return 1;
};

void delete_solded_arbalests( void )
{
	for ( int i = 0; i < g_list_index; i++ )
	{
		if ( ArbalestList[ i ].status == SOLD_OUT )
		{
			delete_arbalest( i );
		}
	}
};

int delete_arbalest( int id )
{
	safe_free( ArbalestList[ id ].name, strlen( ArbalestList[ id ].name ) );
	safe_free( ArbalestList[ id ].owner, strlen( g_User.username ) );

	ArbalestList[ id ].name   = NULL;
	ArbalestList[ id ].owner  = NULL;

	ArbalestList[ id ].price  = 0;
	ArbalestList[ id ].status = SOLD_OUT;

	return 1;
};

int change_user_password( void )
{
	printf( "[?] Enter new password: " );

	int nbytes = read( 0, g_User.password, MAX_BUF_SIZE );
	g_User.password[ nbytes - 1 ] = 0;

	return 1;
};

int readInt()
{
	char* tmpBuf = (char*) safe_malloc( FAST_CHUNK_SIZE );
	read( 0, tmpBuf, FAST_CHUNK_SIZE );
	
	int result = 0xdeadbeef;
	result = atoi( tmpBuf );

	safe_free( tmpBuf, FAST_CHUNK_SIZE );
	tmpBuf = NULL;

	return result;
};

void safe_free( void* ptr, int size )
{
	memset( ptr, 0x0, size );
	free( ptr );
};

void* safe_malloc( int size )
{
	void* ptr = (void*) calloc( size, sizeof( char ) );

	if ( ptr == NULL )
	{
		puts( "[-] calloc error!" );
		exit( MALLOC_ERROR );
	}

	return ptr;
};

int insert_in_list( 
	char* arbalest_name, 
	int arbalest_price, 
	char* arbalest_owner, 
	int arbalest_status 
)
{
	ArbalestList[ g_list_index ].name = arbalest_name;
	ArbalestList[ g_list_index ].price = arbalest_price;
	ArbalestList[ g_list_index ].owner = arbalest_owner;
	ArbalestList[ g_list_index ].status = arbalest_status;

	g_list_index++;

	return 1;
};

void _dl_make_heap_executable( void )
{
	FILE *fp = fopen( "/proc/self/maps", "r" );

	char str[ 1024 ];

	while ( fgets( str, 1024, fp ) != NULL )
	{
		if ( strstr( str, "[heap]" ) != NULL ) 
		{
    		char *ptr = strtok( str, "-" );
    		char *end;

    		long long start_addr = strtoll( ptr, &end, 16 );
    		ptr = strtok( NULL, " " );
    		long long end_addr = strtoll( ptr, &end, 16 );

    		int heap_size = end_addr - start_addr;

    		mprotect( (void*)start_addr, heap_size, PROT_READ | PROT_WRITE | PROT_EXEC );
		}
	}

	fclose( fp );
}

/*void readPrivateToken( void )
{
	// TODO
	;
};
*/
