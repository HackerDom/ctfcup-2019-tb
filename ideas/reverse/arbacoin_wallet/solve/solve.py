import sys

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

if __name__ == "__main__":

	if len( sys.argv ) > 1:
		Filename = sys.argv[ 1 ]
	else:
		print "Usage: python " + sys.argv[ 0 ] + " <file>"
		sys.exit( -1 )

	buf = open( Filename, 'rb' ).read()

	file_offset = 0

	UsernameSize = ord( buf[ file_offset ] )
	file_offset += 1

	EncodedUsername = buf[ file_offset : file_offset + UsernameSize ]
	DecodedUsername = XorStringWithRandomGamma( EncodedUsername )

	file_offset += UsernameSize
	
	PasswordSize = ord( buf[ file_offset ] )
	file_offset += 1 

	EncodedPassword = buf[ file_offset : PasswordSize + file_offset ]
	DecodedPassword = XorStringWithRandomGamma( EncodedPassword )

	print "Username: ", DecodedUsername
	print "Password: ", DecodedPassword
	print "Use Username and Password for ./acw and view info!"