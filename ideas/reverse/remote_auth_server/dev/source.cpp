#include <iostream>
#include <string>
#include <fstream>
#include <vector>

#include <openssl/sha.h>

#include <signal.h>
#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>

#include "sha256.h"

#define OTP_CODE_TIME 15

std::string sha256( const std::string str );
bool CheckUsername( std::string Username );
bool CheckPassword( std::string Password );
bool UsernameValidation( std::string Username );
bool PasswordValidation( std::string Password );
int GenOneTimeCode( std::string, std::string );
void AdminMenu( void );
void ShowAdminInfo( void );
void handle_alarm( int code );
void ReadFile( std::string Filename );
std::vector<int> hex2int_vec( std::string Src );

// this is sha256 hash of admin123
// password: KlRycdNKJ62qXDPA2kDUXgqtSIeJ2nGT
int username_hash[] = {36,11,229,24,250,189,39,36,221,182,240,78,235,29,165,150,116,72,215,232,49,192,140,143,168,34,128,159,116,199,32,169};
char alph[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

int main( int argc, char* argv[], char* envp[] )
{
	std::cout << "Username: ";

	std::string Username;
	std::cin >> Username; 

	if ( !CheckUsername( Username ) )
	{
		std::cout << "[-] Username error!" << std::endl;
		return -1; 
	}
	
	if ( !UsernameValidation( Username ) )
	{
		return -1;
	}

	std::cout << "Password: ";

	std::string Password;
	std::cin >> Password;

	if ( !CheckPassword( Password ) )
	{
		std::cout << "[-] Password error" << std::endl;
		return -1;
	}

	if ( !PasswordValidation( Password ) )
	{
		return false;
	}

	int OneTimeCode;
	OneTimeCode = GenOneTimeCode( Username, Password );

	std::cout << "[+] Otp-code will be send to admin email!" << std::endl;
	std::cout << "[?] Enter the otp-code: ";

	signal( SIGALRM, handle_alarm );
    alarm( OTP_CODE_TIME ); 

	int UserOtpCode;
	std::cin >> UserOtpCode;

	if ( UserOtpCode != OneTimeCode )
	{
		std::cout << "[-] Otp-code error!" << std::endl;
		return -1;
	}

	AdminMenu();
	return 0;
};

void ShowAdminInfo( void )
{
	ReadFile( "server_info.txt" );
};

void AdminMenu( void )
{
	while ( 1 )
	{
		std::cout << "--- Admin Panel ---" << std::endl;
		std::cout << "1. Show account info" << std::endl;
		std::cout << "2. Give shell (in progress)" << std::endl;
		std::cout << "3. View targets info (in progress)" << std::endl;
		std::cout << "4. View wallet balance (in progress)" << std::endl;
		std::cout << "5. Exit" << std::endl;
		std::cout << "Enter option: ";

		int option;
		std::cin >> option;

		switch( option )
		{
			case 1:
				ShowAdminInfo();
			case 2:
			case 3:
			case 4:
				break;
			case 5:
				exit( -1337 );
			default:
			{
				std::cout << "[-] Error option!" << std::endl;
				exit( -1338 );
			}
		}
	}

};

int GenOneTimeCode( std::string Username, std::string Password )
{
	unsigned long seed = time( NULL ) + (int) Username[ 0 ] + (int) Password[ 0 ];
	seed += Username.size() + Password.size();
	seed ^= 0xdeadbeef;

	srand( seed );

	int OTPcode = rand() & 0xffffff;

	return OTPcode;
};

bool CheckPassword( std::string Password )
{
	for ( auto chr : Password )
	{
		if ( !isprint( chr ) )
			return false;
	}

	if ( Password.size() != 32 )
	{
		return false;
	}

	return true;
};

bool PasswordValidation( std::string Password )
{
	std::string internal_password = Password;

	for ( int i = 0; i < Password.size(); i++ )
	{
		
		internal_password[ i ] = alph[ username_hash[ i ] % 62 ];

		if ( internal_password[ i ] != Password[ i ] )
		{
			std::cout << "[-] Invalid Password!" << std::endl;
			return false;
		}
	}

	return true;
};

bool CheckUsername( std::string Username )
{
	for ( auto chr : Username )
	{
		if ( !isprint( chr ) )
			return false;	
	}

	if ( Username.size() != 8 )
	{
		return false;
	}

	return true;
};

bool UsernameValidation( std::string Username )
{
	std::string UsernameSha256Hash = sha256( Username );

	std::vector<int> IntHash;
	IntHash = hex2int_vec( UsernameSha256Hash );

	int InternalHashSize = sizeof( username_hash ) / sizeof( int );

	if ( IntHash.size() != InternalHashSize )
	{
		std::cout << "[-] Some internal error! Tell admin!" << std::endl;
		return false;
	}

	for ( int i = 0; i < IntHash.size(); i++ )
	{
		if ( IntHash[ i ] != (char) username_hash[ i ] )
		{
			std::cout << "[-] Incorrect username!" << std::endl;
			return false;
		}
	}

	return true;
};

void handle_alarm( int code )
{
	std::cout << "[-] OTP-code input timeout!" << std::endl;
    exit( 1337 );
};

void ReadFile( std::string Filename )
{
	std::string line;
	std::ifstream file ( Filename );

	if ( file.is_open() )
	{
		while ( getline ( file, line ) )
		{
			std::cout << line << std::endl;
		}
	
		file.close();
	}

	else 
	{
		std::cout << "[-] Error in file <" << Filename << "> open!" ;
		std::cout << std::endl;
		std::cout << "[!] Tell admin!" << std::endl;
	}
};

std::vector<int> hex2int_vec( std::string Src )
{
	std::vector<int> result;

	for( int i = 0; i< Src.size(); i += 2 )
	{
    	std::string byte = Src.substr( i, 2 );
    	char chr = (char) (int)strtol( byte.c_str(), NULL, 16 );

    	result.push_back(chr);
	}

	return result;
}