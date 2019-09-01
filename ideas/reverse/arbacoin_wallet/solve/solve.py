import sys

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
	DecodedUsername = ''

	for i in EncodedUsername:
		DecodedUsername += chr( ord( i ) ^ UsernameSize ) 

	file_offset += UsernameSize
	print "Username: ", DecodedUsername

	PasswordSize = ord( buf[ file_offset ] )
	file_offset += 1 

	EncodedPassword = buf[ file_offset : PasswordSize + file_offset ]
	DecodedPassword = ''

	for i in EncodedPassword:
		DecodedPassword += chr( ord( i ) ^ PasswordSize )

	print "Password: ", DecodedPassword

	print "Use Username and Password for ./acw and view info!"