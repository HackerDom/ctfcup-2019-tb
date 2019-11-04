#!/usr/bin/env python3

from os import urandom
from hashlib import sha1
from Crypto.Util.number import GCD, getPrime, inverse, long_to_bytes, bytes_to_long


class RSA(object):
    def __init__(self, key):
        self._n, self._e, self._d = key
        self._digest = sha1(b'').digest()

    @staticmethod
    def generate(bits, e):
        p, q = getPrime(bits), getPrime(bits)
        n = p * q
        phi = (p - 1) * (q - 1)
        assert GCD(e, phi) == 1
        d = inverse(e, phi)
        return RSA((n, e, d))

    @property
    def publickey(self):
        return self._n, self._e

    @property
    def size(self):
        return (self._n.bit_length() + 7) // 8

    def encrypt(self, plaintext):
        size = 20
        max_length = self.size - 2 * size - 2
        plaintext = plaintext[:max_length]
        seed = urandom(size)
        salt = self._digest + b'\x00' * (max_length - len(plaintext)) + b'\x01' + plaintext
        salted_seed = self._xor(salt, self._expand(seed, self.size - size - 1))
        xored_seed = self._xor(seed, self._expand(salted_seed, size))
        return self._encrypt(b'\x00' + xored_seed + salted_seed)

    def decrypt(self, ciphertext):
        size = 20
        message = self._decrypt(ciphertext)
        xored_seed = message[:size]
        salted_seed = message[size:]
        seed = self._xor(xored_seed, self._expand(salted_seed, size))
        salt = self._xor(salted_seed, self._expand(seed, self.size - size))
        return salt[salt.find(b'\x00\x01', salt.find(self._digest)) + 2:]

    def _as_bytes(inner_func):
        def new_func(self, raw_data):
            data = bytes_to_long(raw_data)
            result = inner_func(self, data)
            return long_to_bytes(result)
        return new_func

    @_as_bytes
    def _encrypt(self, plaintext):
        return pow(plaintext, self._e, self._n)

    @_as_bytes
    def _decrypt(self, ciphertext):
        return pow(ciphertext, self._d, self._n)

    def _xor(self, data1, data2):
        return bytes(x^y for x, y in zip(data1, data2))

    def _expand(self, data, length):
        result = b''
        counter = 0
        while len(result) < length:
            current = counter.to_bytes(4, 'big')
            result += sha1(data + current).digest()
            counter += 1
        return result[:length]
