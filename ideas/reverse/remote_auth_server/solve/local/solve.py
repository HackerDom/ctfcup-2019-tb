from pwn import *

LOCAL = False

host = '127.0.0.1'
port = 1337


Username = 'admin123' # retrive from sha256-hash in programm
Password = 'KlRycdNKJ62qXDPA2kDUXgqtSIeJ2nGT' # retrive from function PasswordValidation()

def GenOtpCode():
	p = process( "./gen_otp" )
	number = int( p.recv() )
	p.close()

	return number

if __name__ == "__main__":

	if LOCAL:
		p = process( "./ras" )
	else:
		p = remote( host, port )

	p.recvuntil( ": " )
	p.send( Username + "\n" )

	p.recvuntil( ": " )
	p.send( Password + "\n" )

	p.recvuntil( ": " )

	OTPcode = GenOtpCode()

	p.send( str( OTPcode ) + "\n" )

	p.interactive()
