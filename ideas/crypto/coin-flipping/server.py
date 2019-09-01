#!/usr/bin/env python3

import json

from os import urandom
from signal import alarm
from collections import OrderedDict

from random import shuffle
from hashlib import sha512
from fastecdsa.curve import P521
from Crypto.Util.number import long_to_bytes, bytes_to_long


class Cipher(object):
    def __init__(self, key, curve):
        self._key = bytes_to_long(key)
        self._P, self._Q = self._get_points(curve)

    def crypt(self, text):
        block = self._generate_block(len(text))
        return self._xor(text, block)

    def _get_points(self, curve):
        P = curve.G
        Q = 31337 * P
        return P, Q

    def _generate_block(self, size):
        data = b''
        for number in self._expand_key():
            data += long_to_bytes(number)
            if len(data) >= size:
                break
        return data[:size]

    def _expand_key(self):
        while True:
            self._key = (self._key * self._P).x
            yield (self._key * self._Q).x

    def _xor(self, block1, block2):
        return bytes(x^y for x, y in zip(block1, block2))


# https://en.wikipedia.org/wiki/Commitment_scheme#Coin_flipping

class CoinFlipping(object):
    WIN, LOSE = 0, 1

    def __init__(self, cipher):
        self._cipher = cipher
        self._keys = ['heads', 'tails']
        self._values = ['you win', 'you lose']

    def play(self, iterations):
        for i in range(iterations):
            print('[*] Round %d.' % i)
            options = [self.WIN, self.LOSE]
            shuffle(options)
            obj_text, sign = self._build_obj(options)
            print('[+] Bets are made. Sign: %s' % sign)
            print('[?] Please, flip a coin (%s): ' % '/'.join(self._keys))
            result = input().lower()
            if result not in self._keys:
                raise Exception('unknown result')
            print('[*] Bets was: %s' % repr(obj_text))
            print('[*] You can proof it by taking a hash.')
            if self._keys.index(result) != options.index(self.WIN):
                return False
            print('[+] Good.\n')
        return True

    def _build_obj(self, options):
        obj = OrderedDict()
        for i in range(len(options)):
            obj[self._keys[options[i]]] = self._values[i]
        digest = sha512(json.dumps(obj).encode()).digest()
        obj['unique'] = self._cipher.crypt(digest).hex()
        obj_text = json.dumps(obj).encode()
        sign = sha512(obj_text).hexdigest()
        return obj_text, sign


def main(flag):
    key = urandom(64)
    cipher = Cipher(key, P521)
    flipping = CoinFlipping(cipher)
    if flipping.play(50):
        print('\n[+] You win!')
        print('[!] %s' % flag)
    else:
        print('\n[-] You lose!')
        print('[*] Bye.')


if __name__ == '__main__':
    alarm(60)
    with open('flag.txt', 'r') as file:
        flag = file.read().strip()
    try:
        main(flag)
    except Exception as e:
        print('[-] %s' % str(e))
