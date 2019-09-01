import wallet_gen
import random
import os

FLAG = 'Cup{901caa40579a07ee5912514eebaf5526742ad03261971b233fd1cb88eee915ae}'

if __name__ == "__main__":
	username = wallet_gen.idg()
	password = wallet_gen.idg()

	wallet = wallet_gen.Wallet( username, password, FLAG )

	wallet.pack_file( "test_file" )
	buf = open( 'test_file', 'rb' ).read()
	
	print buf.encode( 'hex' )

	os.system( "rm test_file" )