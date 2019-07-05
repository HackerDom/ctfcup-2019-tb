#!/usr/bin/python3

import sys

from protocol.io import SimpleIO, EncryptedIO


def check_flag(attempt):
    with open('flag.txt', 'rb') as file:
        flag = file.read()

    return flag.strip() == attempt.strip()


def main():
    io = SimpleIO()
    io = EncryptedIO(io)

    io.print(b'[*] Please, input your flag:')
    flag = io.input()

    io.print(b'[*] Checking %s ...' % flag)
    
    if check_flag(flag):
        io.print(b'[+] Correct :)')
    else:
        io.print(b'[-] Wrong :(')

    io.print(b'[*] Bye!')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e, file=sys.stderr)
