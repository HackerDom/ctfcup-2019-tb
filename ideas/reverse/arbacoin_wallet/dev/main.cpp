#include "main.h"

int main( int argc, char* argv[], char* envp[] )
{
	std::string InputFilename( "default.acw" );

	if ( argc > 1 )
	{
		InputFilename = std::string( argv[ 1 ] );
	}
	else
	{
		std::cout << "Usage: ./acw <wallet>" << std::endl;  
		return USAGE_ERROR;
	}

	Wallet wallet = Wallet( InputFilename );

	std::string Username;
	std::cout << "Enter login: ";
	std::cin >> Username;

	std::string Password;	
	std::cout << "Enter password: ";
	std::cin >> Password;

	if ( !wallet.SetUsername( Username ) )
	{
		std::cout << "[-] Some error in login set!" << std::endl;
		return LOGIN_SET_ERROR;
	}

	if ( !wallet.SetPassword( Password ) )
	{
		std::cout << "[-] Some error in password set!" << std::endl;
		return PASSWORD_SET_ERROR;
	}

	if ( !wallet.Decrypt() )
	{
		std::cout << "[-] Invalid login or password!" << std::endl;
		return INVALID_LOGIN_OR_PASSWORD;
	}

	while ( 1 )
	{		
		std::cout << "-- Menu --" << std::endl;
		std::cout << "1. View balance" << std::endl;
		std::cout << "2. View last operations" << std::endl;
		std::cout << "3. View info" << std::endl;
		std::cout << "4. Exit" << std::endl;
		std::cout << ">> ";
		
		int Option;

		std::cin >> Option;

		switch( Option )
		{
			case 1:
				std::cout << "Balance: " << wallet.GetBalance() << std::endl;
				break;
			case 2:
				wallet.ViewLastOperations();
				break;
			case 3:
				std::cout << "Info: " << wallet.GetInfo() << std::endl;
				break;
			case 4:
				exit( NORMAL_EXIT );
			default:
				std::cout << "[-] Error option!" << std::endl;
				exit( NO_OPTION );
		}
	}

	return 0;	
};