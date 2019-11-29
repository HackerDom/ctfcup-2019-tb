#!/usr/bin/env python3

import sys
import params

from protocol import IO, NoEncryption, RSAEncryption


def select_cipher():
    print('[*] Please, select encryption mode:')
    print('[0] No encryption')
    print('[1] RSA')
    choice = int(input())
    if choice == 0:
        return NoEncryption()
    if choice == 1:
        io = IO(sys.stdin.buffer, sys.stdout.buffer)
        return RSAEncryption(io, params)
    raise Exception('encryption mode is not implemented')


def main(flag):
    cipher = select_cipher()
    print(cipher.encrypt('[*] Please, input your flag:'))
    attempt = cipher.decrypt(input()).strip()
    print(cipher.encrypt('[*] Checking %s ...' % attempt))
    if len(attempt) != len(flag):
        print(cipher.encrypt('[-] Incorrect length :('))
    elif attempt != flag:
        print(cipher.encrypt('[-] Wrong :('))
    else:
        print(cipher.encrypt('[+] Correct :)'))
    print(cipher.encrypt('[*] Bye!'))


if __name__ == '__main__':
    with open('flag.txt', 'r') as file:
        flag = file.read().strip()
    try:
        main(flag)
    except Exception as e:
        print('[-] %s' % e)
