import sys
import struct
import random

p32 = lambda val : struct.pack( "!L", val )
BLANCE_KEY = 0xdeadbeef

FLAG = 'Cup{901caa40579a07ee5912514eebaf5526742ad03261971b233fd1cb88eee915ae}'
templates = ['debiting from the account %d arbc to %s account', 
'crediting from %s to a wallet %d arbc']

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'

def idg( size = 16, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )

def GenRandomValue( seed ):
    S = seed

    S = ((((S >> 31) ^ (S >> 30) ^ (S >> 29) ^ (S >> 27) ^ (S >> 25) ^ S ) & 0x00000001 ) << 31 ) | (S >> 1)

    return S & 0xff

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
		for i in range( 10, random.randint( 11, 40 ) ):

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

	Username = idg( random.randint( 16, 32 ) )
	Password = idg( random.randint( 32, 64 ) )

	wallet = Wallet( Username, Password, FLAG )

	wallet.pack_file( "test_wallet.acw" )

