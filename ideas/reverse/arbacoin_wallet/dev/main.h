#include <iostream>
#include <string>
#include <vector>
#include <iterator>
#include <fstream>

#define USAGE_ERROR 0x101
#define FILE_OPEN_ERROR 0x102
#define LOGIN_SET_ERROR 0x103
#define PASSWORD_SET_ERROR 0x104
#define INVALID_LOGIN_OR_PASSWORD 0x105
#define NORMAL_EXIT 0x106
#define NO_OPTION 0x107

#define BALANCE_XOR_KEY 0xdeadbeef

typedef unsigned char BYTE;
typedef unsigned int DWORD;

std::vector<BYTE> ReadFile( std::string );

class Wallet {
	private:
		std::string Name;
		int balance;
		std::string Info;
		std::vector<std::string> last_operations;

		std::string Username;
		std::string Passsword;

		std::vector<BYTE> RawData;

	public:
		Wallet( std::string Filename );
		//~Wallet( void );

		void ViewBasicInfo( void );
		bool Decrypt( void );
		void ViewLastOperations( void );
		int GetBalance( void );
		std::string GetInfo( void );
		std::vector<BYTE> GetRawData( void );

		bool SetUsername( std::string );
		bool SetPassword( std::string );
};

Wallet::Wallet( std::string Filename )
{
	Name = Filename;
	RawData = ReadFile( Filename );
};

std::vector<BYTE> Wallet::GetRawData( void )
{
	return RawData;
};

std::vector<BYTE> ReadFile( std::string Filename )
{
	std::ifstream InputFile ( Filename, std::ios::binary | std::ios::ate );

	// check file is exist and opened
	if ( !InputFile.is_open() )
	{
		std::cout << "[-] Error in file <" << Filename << "> open!";
		std::cout << std::endl;

		exit( FILE_OPEN_ERROR );
	}

	// get file size
	std::streamsize FileSize = InputFile.tellg();

    // make buffer for file data
    char* TempFileDataBuffer = new char[ FileSize ];

    // set position to start and read in tmp-buffer
    InputFile.seekg( 0, std::ios::beg );
	InputFile.read( TempFileDataBuffer, FileSize );

	InputFile.close();

	std::vector<BYTE> FileData;

	for ( int i = 0; i < FileSize; i++ )
	{
		FileData.push_back( TempFileDataBuffer[ i ] );
	}

	delete[] TempFileDataBuffer;

	return FileData;
};

bool Wallet::SetUsername( std::string InpUsername )
{
	if ( InpUsername.size() > 32 )
	{
		return false;
	}

	Username = InpUsername;

	return true;
};

bool Wallet::SetPassword( std::string InpPassword )
{
	if ( InpPassword.size() > 64 )
	{
		return false;
	}

	Passsword = InpPassword;

	return true;
};

bool Wallet::Decrypt( void )
{
	int file_offset = 0;

	int OriginalUsernameSize = (int) RawData[ file_offset ];
	file_offset += 1;

	// check username
	if ( OriginalUsernameSize != Username.size() )
	{
		return false;
	}

	for ( int i = 0; i < OriginalUsernameSize; i++ )
	{
		if ( ( RawData[ file_offset + i ] ^ OriginalUsernameSize ) != Username[ i ] )
		{
			return false;
		}
	}

	file_offset += OriginalUsernameSize;

	// check password
	int OriginalPasswordSize = (int) RawData[ file_offset ];
	file_offset += 1;

	if ( OriginalPasswordSize != Passsword.size() )
	{
		return false;
	}

	for ( int i = 0; i < OriginalPasswordSize; i++ )
	{
		if ( ( RawData[ file_offset + i ] ^ OriginalPasswordSize ) != Passsword[ i ] )
		{
			return false;
		}
	}

	file_offset += OriginalPasswordSize;

	// get balance
	char tmp_buffer[ 4 ];
	tmp_buffer[ 0 ] = RawData[ file_offset + 3 ];
	tmp_buffer[ 1 ] = RawData[ file_offset + 2 ];
	tmp_buffer[ 2 ] = RawData[ file_offset + 1 ];
	tmp_buffer[ 3 ] = RawData[ file_offset ];
	file_offset += 4;

	memcpy( &balance, tmp_buffer, 4 );
	balance ^= BALANCE_XOR_KEY;

	// get operations
	int OperationsSize = (int) RawData[ file_offset ];
	file_offset += 1;

	for ( int i = 0; i < OperationsSize; i++ )
	{
		int EntrySize = (int) RawData[ file_offset ];
		file_offset += 1;

		std::string Operation( EntrySize, ' ' );

		for ( int j = 0; j < EntrySize; j++ )
			Operation[ j ] = RawData[ file_offset + j ] ^ EntrySize;
		
		file_offset += EntrySize;
		last_operations.push_back( Operation );
	}

	// get info
	int InfoSize = (int) RawData[ file_offset ];
	file_offset += 1;

	std::string XorKey = Username + Passsword;
	std::string DecodedInfo( InfoSize, ' ' );

	for ( int i = 0; i < InfoSize; i++ )
	{
		DecodedInfo[ i ] = RawData[ file_offset + i ] ^ XorKey[ i % XorKey.size() ];
	}

	Info = DecodedInfo;

	return true;
};

int Wallet::GetBalance( void )
{
	return balance;
};

std::string Wallet::GetInfo( void )
{
	return Info;
};

void Wallet::ViewLastOperations( void )
{
	std::cout << "--- Last Operations ---" << std::endl;

	for ( int i = 0; i < last_operations.size(); i++ )
	{
		std::cout << i << ". " << last_operations[ i ] << std::endl;
	}
};
