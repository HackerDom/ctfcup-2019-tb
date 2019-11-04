#!/usr/bin/env python3

from os import urandom
from hashlib import sha256


class HMAC(object):
    block_size = 64

    def __init__(self, key):
        self._key = key
        self._ipad = b'\x36' * HMAC.block_size
        self._opad = b'\x5c' * HMAC.block_size

    @staticmethod
    def generate():
        key = urandom(HMAC.block_size)
        key = key.rjust(HMAC.block_size, b'\x00')
        return HMAC(key)

    @property
    def publickey(self):
        return self._ipad, self._opad

    def encrypt(self, plaintext):
        k_ipad = self._xor(self._key, self._ipad)
        k_opad = self._xor(self._key, self._opad)
        return sha256(k_opad + sha256(k_ipad + plaintext).digest()).digest()

    def decrypt(self, ciphertext):
        raise NotImplementedError('decryption is not implemented')

    def _xor(self, data1, data2):
        return bytes(x^y for x, y in zip(data1, data2))
