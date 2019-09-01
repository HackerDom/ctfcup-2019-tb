import sys
import struct
import random

p32 = lambda val : struct.pack( "!L", val )
BLANCE_KEY = 0xdeadbeef

FLAG = 'Cup{901caa40579a07ee5912514eebaf5526742ad03261971b233fd1cb88eee915ae}'
templates = ['debiting from the account %d arbc', 
'crediting to a wallet %d arbc']

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'

def idg( size = 12, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )

class Wallet:
	login = None
	password = None
	balance = None
	last_operations = []
	info = None

	def __init__( self, Username, Password, _info ):
		self.login = Username
		self.password = Password
		self.balance = random.randint( 1024, 1024 ** 2 )
		self.gen_random_operations()

		self.info = _info

	def gen_random_operations( self ):
		global templates
		for i in range( 1, random.randint( 2, 20 ) ):
			self.last_operations.append( templates[ random.randint( 0, 1 ) ] % random.randint( 1, 512 ) )

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

		for i in range( len( self.login ) ):
			fd.write( chr( ord( self.login[ i ] ) ^ len( self.login ) ) )

		fd.write( chr( len( self.password ) ) )

		for i in range( len( self.password ) ):
			fd.write( chr( ord( self.password[ i ] ) ^ len( self.password ) ) )

		self.balance ^= BLANCE_KEY
		fd.write( p32( self.balance ) )

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

	Username = 'Admin'
	Password = 'Password'

	wallet = Wallet( Username, Password, FLAG )

	wallet.pack_file( "test_file" )

