#!/usr/bin/env python3

from os import urandom
from Crypto.Cipher import Blowfish as BlowfishCipher


class Blowfish(object):
    block_size = BlowfishCipher.block_size

    def __init__(self, cipher):
        self._cipher = cipher

    @staticmethod
    def generate(bits):
        key = urandom(bits // 8)
        key = key.rjust(Blowfish.block_size * 4, b'\x00')
        cipher = BlowfishCipher.new(key[:Blowfish.block_size*4], mode=BlowfishCipher.MODE_ECB)
        return Blowfish(cipher)

    @property
    def publickey(self):
        raise NotImplementedError('public key does not exist')

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        ciphertext = b''
        for i in range(0, len(plaintext), Blowfish.block_size):
            block = plaintext[i:i+Blowfish.block_size]
            iv = urandom(Blowfish.block_size)
            ciphertext += self._cipher.encrypt(iv)
            ciphertext += self._xor(iv, self._cipher.encrypt(block))
        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % Blowfish.block_size != 0:
            ciphertext = self._pad(ciphertext)
        plaintext = b''
        for i in range(0, len(ciphertext), Blowfish.block_size * 2):
            iv, block = ciphertext[i:i+Blowfish.block_size], ciphertext[i+Blowfish.block_size:i+Blowfish.block_size*2]
            plaintext += self._cipher.decrypt(self._xor(self._cipher.decrypt(iv), block))
        return self._unpad(plaintext)

    def _pad(self, text):
        char = Blowfish.block_size - len(text) % Blowfish.block_size
        return text + bytes([char]) * char

    def _unpad(self, text):
        if len(text) == 0:
            return text
        return text[:-text[-1]]

    def _xor(self, data1, data2):
        return bytes(x^y for x, y in zip(data1, data2))
