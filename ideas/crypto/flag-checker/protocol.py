#!/usr/bin/env python3

from gmpy2 import invert, next_prime
from random import getrandbits


def make_prime(nbits):
    return int(next_prime(getrandbits(nbits)))


def long_to_bytes(n):
    bitlen = n.bit_length()
    nbits = (bitlen + 7) >> 3
    return n.to_bytes(nbits, 'big')


def bytes_to_long(b):
    return int.from_bytes(b, 'big')


class NoEncryption(object):
    def encrypt(self, text):
        return text

    def decrypt(self, text):
        return text


class RSAEncryption(object):
    def __init__(self, io, params):
        self._rsa = self._init_rsa(io, params)

    def encrypt(self, text):
        pt = bytes_to_long(text.encode())
        return str(self._rsa.encrypt(pt))

    def decrypt(self, text):
        ct = self._rsa.decrypt(int(text))
        return long_to_bytes(ct).decode()

    def _init_rsa(self, io, params):
        p = self._dh_init_key(io, params.DH)
        q = self._dh_init_key(io, params.DH)
        rsa = RSA(p, q, params.RSA.e)
        return rsa

    def _dh_init_key(self, io, params):
        dh = DH(params.g, params.p, params.nbits)
        io.write(str(dh.get_public()))
        other_public = int(io.read())
        key = dh.get_key(other_public)
        return int(next_prime(key))


class DH(object):
    def __init__(self, g, p, nbits):
        self._g, self._p = g, p
        self._generate(nbits)

    def get_public(self):
        return self._public

    def get_key(self, other_public):
        return pow(other_public, self._secret, self._p)

    def _generate(self, nbits):
        self._secret = make_prime(nbits)
        self._public = pow(self._g, self._secret, self._p)


class RSA(object):
    def __init__(self, p, q, e):
        self._n = p * q
        self._e = e
        self._d = self._compute_d(p, q, e)

    def encrypt(self, m):
        self._check_bounds(m)
        return pow(m, self._e, self._n)

    def decrypt(self, c):
        self._check_bounds(c)
        return pow(c, self._d, self._n)

    def _compute_d(self, p, q, e):
        phi = (p - 1) * (q - 1)
        return int(invert(e, phi))

    def _check_bounds(self, number):
        if abs(number) >= self._n:
            raise Exception('message is too long')


class IO(object):
    def __init__(self, stdin, stdout):
        self._stdin = stdin
        self._stdout = stdout

    def read(self):
        self._stdin.flush()
        line = self._stdin.readline()[:-1]
        return line.decode()

    def write(self, line):
        self._stdout.write(line.encode() + b'\n')
        self._stdout.flush()
