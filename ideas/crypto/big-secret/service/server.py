#!/usr/bin/env python3

from math import gcd
from random import getrandbits
from collections import namedtuple

from gmpy2 import next_prime, invert


PublicKey = namedtuple('PublicKey', ['n', 'e', 'y'])


class TrustCenter(object):
    def __init__(self, bits):
        p = self._generate_prime(bits)
        q = self._generate_prime(bits)
        self._n = p * q
        self._phi = (p - 1) * (q - 1)

    def make_public_key(self, secret, exponent):
        if self._check_secret(secret) and self._check_exponent(exponent):
            y = pow(secret, exponent, self._n)
            return PublicKey(self._n, exponent, y)

    def _check_secret(self, secret):
        if abs(secret) >= self._n:
            raise Exception('abs(secret) >= n')
        return True

    def _check_exponent(self, exponent):
        if not 1 < exponent < self._phi:
            raise Exception('not 1 < exponent < phi')
        if gcd(exponent, self._phi) != 1:
            raise Exception('gcd(exponent, phi) != 1')
        return True

    def _generate_prime(self, bits):
        return int(next_prime(getrandbits(bits)))


class GuillouQuisquater(object):
    def __init__(self, bits, secret, public_key):
        self._bits = bits
        self._secret = secret
        self._key = public_key
        self._r = self._generate_multiplier()
        self._a = pow(self._r, self._key.e, self._key.n)

    def get_public_multiplier(self):
        return self._a

    def compute_witness(self, c):
        if not 0 <= c <= self._key.e - 1:
            raise Exception('not 0 <= c <= e - 1')
        return (self._r * pow(self._secret, c, self._key.n)) % self._key.n

    def _generate_multiplier(self):
        r = 0
        while not 1 <= r <= self._key.n - 1:
            r = getrandbits(self._bits) ^ \
                getrandbits(self._bits)
        return int(invert(r, self._key.n))


def interact(bits, secret, public_key):
    print('public_key:', public_key)
    while True:
        print('\n=== VERIFICATION ROUND ===')
        gq = GuillouQuisquater(bits, secret, public_key)
        print('a:', gq.get_public_multiplier())
        c = int(input('c: '))
        print('z:', gq.compute_witness(c))
        print('now check that z ** e == a * (y ** c) (mod n)')
        if not input('again? (y/n): ').lower().startswith('y'):
            break
    print('Bye!')


def main(flag):
    bits = 1024
    exponent = 31337
    secret = int(flag.hex(), 16)
    tc = TrustCenter(bits)
    public_key = tc.make_public_key(secret, exponent)
    interact(bits, secret, public_key)


if __name__ == '__main__':
    with open('flag.txt', 'rb') as file:
        flag = file.read()
    try:
        main(flag)
    except Exception as e:
        print('Error:', e)
