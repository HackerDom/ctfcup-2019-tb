#!/usr/bin/env python3

from ui import UI
from random import randint
from ciphers import AES, RSA, HMAC, Blowfish


def main(flag):
    print('[?] Please, input crypto security level:')
    level = int(input())
    if level < 512:
        print('[-] Your level is too weak :(')
        return
    if level > 4096:
        print('[-] Your level is too strong :(')
        return
    ciphers = [
        AES.generate(level),
        RSA.generate(level, 0x10001),
        HMAC.generate(level),
        Blowfish.generate(level)
    ]
    ui = UI(ciphers, flag)
    ui.run()


if __name__ == '__main__':
    with open('flag.txt', 'rb') as file:
        flag = file.read()
    try:
        main(flag)
    except Exception as e:
        print(e)
