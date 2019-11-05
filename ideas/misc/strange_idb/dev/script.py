from idaapi import *
from idc import *
import struct

p_8 = lambda val : struct.pack( "!B", val )

if __name__ == "__main__":

	buf = b''

	buf += p_8( get_db_byte( 0x4178 ) + 0x1d )
	buf += p_8( get_db_byte( 0x4122 ) ) * 2
	buf += p_8( get_db_byte( 0x41A4 ) )
	buf += p_8( get_db_byte( 0x41C7 ) )

	buf += p_8( get_db_byte( 0x43A0 ) ) * 8
	buf += p_8( get_db_byte( 0x43A1 ) )
	buf += p_8( get_db_byte( 0x4104 ) )
	buf += p_8( get_db_byte( 0x4218 ) )

	buf += p_8( get_db_byte( 0x2028 ) )

	buf += p_8( get_db_byte( 0x409c ) )
	buf += p_8( get_db_byte( 0x434c ) )
	buf += p_8( get_db_byte( 0x2052 ) )
	
	buf += p_8( get_db_byte( 0x40e8 ) )
	buf += p_8( get_db_byte( 0x202c ) )

	buf += p_8( get_db_byte( 0x2045 ) )
	buf += p_8( get_db_byte( 0x2049 ) )
	buf += p_8( get_db_byte( 0x204f ) )

	buf += p_8( get_db_byte( 0x41ac ) )
	buf += p_8( get_db_byte( 0x4384 ) )

	buf += p_8( get_db_byte( 0x203a ) )
	buf += p_8( get_db_byte( 0x410c ) )
	buf += p_8( get_db_byte( 0x4280 ) )

	buf += p_8( get_db_byte( 0x4370 ) )
	buf += p_8( get_db_byte( 0x4294 ) )
	buf += p_8( get_db_byte( 0x2027 ) )

	buf += p_8( get_db_byte( 0x42d0 ) )
	buf += p_8( get_db_byte( 0x4228 ) )
	buf += p_8( get_db_byte( 0x204f ) )
	buf += p_8( get_db_byte( 0x2030 ) )

	buf += p_8( get_db_byte( 0x4220 ) )
	buf += p_8( get_db_byte( 0x41a0 ) )
	buf += p_8( get_db_byte( 0x430c ) )

	buf += p_8( get_db_byte( 0x42c4 ) )
	buf += p_8( get_db_byte( 0x201d ) )
	buf += p_8( get_db_byte( 0x4204 ) )
	buf += p_8( get_db_byte( 0x42b8 ) )
	buf += p_8( get_db_byte( 0x202e ) )

	buf += p_8( get_db_byte( 0x41d0 ) )
	buf += p_8( get_db_byte( 0x420c ) )
	buf += p_8( get_db_byte( 0x40f0 ) )

	buf += p_8( get_db_byte( 0x425c ) )
	buf += p_8( get_db_byte( 0x42d4 ) )
	buf += p_8( get_db_byte( 0x42f4 ) )
	buf += p_8( get_db_byte( 0x202a ) )

	buf += p_8( get_db_byte( 0x4268 ) )
	buf += p_8( get_db_byte( 0x4104 ) )
	buf += p_8( get_db_byte( 0x2052 ) )

	buf += p_8( get_db_byte( 0x41f8 ) )
	buf += p_8( get_db_byte( 0x41fc ) )
	buf += p_8( get_db_byte( 0x4084 ) )
	buf += p_8( get_db_byte( 0x4084 ) )

	buf += p_8( get_db_byte( 0x40ec ) )
	buf += p_8( get_db_byte( 0x42d4 ) )
	buf += p_8( get_db_byte( 0x4170 ) )
	buf += p_8( get_db_byte( 0x202b ) )

	buf += p_8( get_db_byte( 0x4240 ) )
	buf += p_8( get_db_byte( 0x201d ) )
	buf += p_8( get_db_byte( 0x40c4 ) )

	buf += p_8( get_db_byte( 0x202f ) )
	buf += p_8( get_db_byte( 0x4234 ) )
	buf += p_8( get_db_byte( 0x201b ) )
	buf += p_8( get_db_byte( 0x2020 ) )

	buf += p_8( get_db_byte( 0x41bc ) )
	buf += p_8( get_db_byte( 0x4182 ) )
	buf += p_8( get_db_byte( 0x4324 ) )

	buf += p_8( get_db_byte( 0x41b0 ) )
	buf += p_8( get_db_byte( 0x2050 ) )
	buf += p_8( get_db_byte( 0x41fc ) )

	buf += p_8( get_db_byte( 0x4164 ) )
	buf += p_8( get_db_byte( 0x4380 ) )
	buf += p_8( get_db_byte( 0x2035 ) )

	buf += p_8( get_db_byte( 0x4348 ) )
	buf += p_8( get_db_byte( 0x4180 ) )
	buf += p_8( get_db_byte( 0x4174 ) )

	buf += p_8( get_db_byte( 0x4398 ) )
	buf += p_8( get_db_byte( 0x420c ) )
	buf += p_8( get_db_byte( 0x40cc ) )
	buf += p_8( get_db_byte( 0x439c ) )

	buf += p_8( get_db_byte( 0x437c ) )
	buf += p_8( get_db_byte( 0x410c ) )
	buf += p_8( get_db_byte( 0x41e8 ) )
	buf += p_8( get_db_byte( 0x2055 ) )

	print( "buf = ", buf )