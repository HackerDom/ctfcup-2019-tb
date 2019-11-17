#!/usr/bin/python

from sys import modules
modules.clear()
del modules

_inp = raw_input
_ev  = eval
err = KeyboardInterrupt

__builtins__.__dict__.clear()
__builtins__ = None

print "Enter 'q' or 'Q' to exit!"

while 1:
    try:
        user_input = _inp( ">>> " )
        
        if user_input.lower() == 'q':
            print "[+] Exit"
            break
        
        print _ev( user_input )

    except err:
        print "[+] Exit!"
        break
    
    except:
        print "[-] Error!"
        continue