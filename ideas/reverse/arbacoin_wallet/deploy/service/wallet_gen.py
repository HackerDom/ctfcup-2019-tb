import sys
import struct
import random

# ERRORS START
INCORRECT_LOGIN = -1
INCORRECT_PASSWORD = -2
FORMAT_FILE_ERROR = -3
# ERRORS END 

p32 = lambda val : struct.pack( "!L", val )
u32 = lambda val : struct.unpack( "!L", val )[ 0 ]

BLANCE_KEY = 0xdeadbeef

FLAG = 'Cup{901caa40579a07ee5912514eebaf5526742ad03261971b233fd1cb88eee915ae}'
templates = ['debiting from this account %d arbc to %s account', 
'crediting from %s to a wallet %d arbc']

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'

def idg( size = 16, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )

def GenRandomValue( seed ):
    return (seed >> 1) & 0xff

def GenGamma( seed, sz ):
    gamma = []

    for i in range( 0, sz ):
        value = GenRandomValue( seed )
        seed += value
        gamma.append( value )

    return gamma

def XorStringWithRandomGamma( string ):
	res = ''

	seed = len( string )
	gamma = GenGamma( seed, seed )

	for i in range( len( gamma ) ):
		res += chr( ord( string[ i ] ) ^ gamma[ i ] )

	return res 

def DecryptWallet( data, login, password ):
	file_offset = 0

	login_size = ord( data[ file_offset ] )

	if login_size < 16 or login_size > 32:
		print "[-] Format file error!"
		return FORMAT_FILE_ERROR

	file_offset += 1

	plain_login = data[ file_offset : file_offset + login_size ]
	plain_login = XorStringWithRandomGamma( plain_login )

	if plain_login != login:
		print '[-] Incorrect login'
		return INCORRECT_LOGIN

	file_offset += login_size	

	password_size = ord( data[ file_offset ] )
	
	if password_size < 32 or password_size > 64:
		print "[-] Format file error!"
		return FORMAT_FILE_ERROR

	file_offset += 1

	plain_password = data[ file_offset : file_offset + password_size ]
	plain_password = XorStringWithRandomGamma( plain_password )
	
	if plain_password != password:
		print "[-] Incorrect password!"
		return INCORRECT_PASSWORD

	file_offset += password_size

	balance = u32( data[ file_offset : file_offset + 4 ] )
	balance ^= BLANCE_KEY

	print "balance = %d" % balance

	file_offset += 4

	last_operations_size = ord( data[ file_offset ] )

	if last_operations_size < 2 or last_operations_size > 60:
		print "[-] Format file error!"
		return FORMAT_FILE_ERROR

	file_offset += 1 
	operations = []

	for i in range( last_operations_size ):

		operation_size = ord( data[ file_offset ] )
		
		if operation_size < 26 or operation_size > 1000:
			print "[-] Format file error!"
			return FORMAT_FILE_ERROR 
			
		file_offset += 1
		tmp = ''

		for j in range( operation_size ):
			tmp += chr( ord( data[ file_offset + j ] ) ^ operation_size )

		operations.append( tmp )
		file_offset += operation_size

	print "-------------- last operations --------------"
	
	for op in operations:
		print op
	
	print "-------------- last operations --------------"

	info_size = ord( data[ file_offset ] )
	file_offset += 1

	if info_size <= 0:
		print "[-] Format file error!"
		return FORMAT_FILE_ERROR

	info = ''
	info_xor_key = plain_login + plain_password

	for i in range( info_size ):
		info += chr( ord( data[ file_offset + i ] ) ^ ord( info_xor_key[ i % len( info_xor_key ) ] ) )

	print "info: %s" % info

	return ( plain_login, plain_password, info, balance, operations )

class Wallet:
	login = None
	password = None
	balance = None
	last_operations = []
	info = None

	def __init__( self, Username, Password, Info ):
		self.login = Username
		self.password = Password
		self.balance = random.randint( 0x0, 0x1000 )
		self.gen_random_operations()

		self.info = Info

	def gen_random_operations( self ):
		global templates
		for i in range( 2, 2 + random.randint( 10, 12 ) ):

			template_id = random.randint( 0, 1 )

			if template_id == 0:
				self.last_operations.append( templates[ template_id ] 
					% ( random.randint( 100, 512 ), idg() ) )
			else:
				self.last_operations.append( templates[ template_id ]
				 % (  idg(), random.randint( 100, 512 ) ) )

	def pack_operations( self ):
		for i in range( len( self.last_operations ) ):			
			operation = list( self.last_operations[ i ] )

			for j in range( len( operation ) ):
				operation[ j ] = chr( ord( operation[ j ] ) ^ len( operation ) ) 

			self.last_operations[ i ] = ''.join( operation )

	def pack_info( self, key ):
		self.info = list( self.info )

		for i in range( len( self.info ) ):
			self.info[ i ] = chr( ord( self.info[ i ] ) ^ ord( key[ i % len( key ) ] ) )

		self.info = ''.join( self.info ) 

	def pack_file( self, filename ):
		self.pack_operations()

		fd = open( filename, 'wb' )

		fd.write( chr( len( self.login ) ) )
		fd.write( XorStringWithRandomGamma( self.login ) )

		fd.write( chr( len( self.password ) ) )
		fd.write( XorStringWithRandomGamma( self.password ) )

		# write balance
		fd.write( p32( self.balance ^ BLANCE_KEY ) )

		if len( self.last_operations ) > 0:
			fd.write( chr( len( self.last_operations ) ) )

			for operation in self.last_operations:
				fd.write( chr( len( operation ) ) )
				fd.write( operation )
		else:
			fd.write( "\x00\x00\x00\x00" )

		self.pack_info( self.login + self.password )

		if len( self.info ) > 0:
			fd.write( chr( len( self.info ) ) )

			fd.write( self.info )
		else:
			fd.write( "\x00\x00\x00\x00" )

		fd.close()

if __name__ == "__main__":

	Username = idg( random.randint( 16, 32 ) )
	Password = idg( random.randint( 32, 64 ) )

	print "Test wallet generation"
	print "Name: %s" % Username
	print "Password: %s" % Password

	wallet = Wallet( Username, Password, 'Private' )
	wallet.pack_file( "test_wallet.acw" )

	fd = open( 'test_wallet.acw', 'rb' )
	buf = fd.read()
	fd.close()

	buf = buf.encode( 'hex' )

	print "hex_view = "
	print buf