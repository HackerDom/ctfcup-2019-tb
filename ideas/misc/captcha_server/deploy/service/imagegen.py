from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import string
import random
import os

template_path = 'template.png'

alph = string.ascii_lowercase + string.ascii_uppercase + string.digits
alph = alph.replace( 'j', '' )
alph = alph.replace( 'J', '' )
alph = alph.replace( 'I', '' )
alph = alph.replace( 'l', '' )
alph = alph.replace( 'i', '' )

def idg( size = 8, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )

def FileRead( Filename ):

	fd = open( Filename, 'rb' )
	buf = fd.read()
	fd.close()

	return buf.encode( 'hex' )

def GetRandomImage():

	img = Image.open( template_path )
	draw = ImageDraw.Draw( img )

	font = ImageFont.truetype( "micross.ttf", 24 )
	
	(x, y) = (60, 56)
	message = idg()
	color = 'rgb(0, 0, 0)' 

	draw.text( ( x, y ), message, fill = color, font = font )
		
	RandomImageName = idg() + idg() + ".png"

	img.save( RandomImageName )

	FileData = FileRead( RandomImageName )

	os.system( "rm " + RandomImageName )

	return FileData, message

if __name__ == "__main__":

	print "DEBUG!"

	GetRandomImage()
