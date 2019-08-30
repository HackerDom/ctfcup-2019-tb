from crccheck.crc import Crc16

if __name__ == "__main__":
	# init crc as X25
	crc_obj = Crc16
	crc_obj._initvalue = 0xffff
	crc_obj._reflect_input = True
	crc_obj._reflect_output = True
	crc_obj._xor_output = 0xffff
	crc_obj._check_result = 0x906E

	# this is values after xor
	valids = [ 49170, 5086, 13122, 9750, 15377, 20382, 25550, 29006, 31141, 40445 ]

	cookie = ''
	valids_idx = 0

	while 1:
		for i in range( 20, 127 ):
			for i1 in range( 20, 127 ):
				test = cookie + chr( i ) + chr( i1 )
				
				if len( cookie ) > 0:
					valid_parts = len( cookie ) / 2
					xor_key = crc_obj.calc( bytearray( cookie[ valid_parts ] ) )
				else:
					xor_key = crc_obj.calc( bytearray( chr( i ) ) )
				
				part_crc = crc_obj.calc( bytearray( test ) )

				if (xor_key ^ part_crc) == valids[ valids_idx ]:
					cookie += chr( i ) + chr( i1 )
					valids_idx += 1
					print "cur_cookie =", cookie 
