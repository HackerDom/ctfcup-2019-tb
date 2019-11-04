#!/usr/bin/env python3

from ui import UI
from random import randint
from ciphers import AES, RSA, HMAC, Blowfish


def main(flag):
    ciphers = [
        AES.generate(),
        RSA.generate(randint(0x210, 0x222), 0x10001),
        HMAC.generate(),
        Blowfish.generate()
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
