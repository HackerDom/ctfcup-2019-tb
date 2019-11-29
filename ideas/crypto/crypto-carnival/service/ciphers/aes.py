#!/usr/bin/env python3

from os import urandom
from Crypto.Cipher import AES as AESCipher


class AES(object):
    block_size = AESCipher.block_size

    def __init__(self, cipher):
        self._cipher = cipher

    @staticmethod
    def generate(bits):
        key = urandom(bits // 8)
        key = key.rjust(AES.block_size, b'\x00')
        cipher = AESCipher.new(key[:AES.block_size], mode=AESCipher.MODE_ECB)
        return AES(cipher)

    @property
    def publickey(self):
        raise NotImplementedError('public key does not exist')

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        ciphertext = b''
        iv = urandom(AES.block_size)
        previous = iv
        for i in range(0, len(plaintext), AES.block_size):
            block = plaintext[i:i+AES.block_size]
            result = self._cipher.encrypt(self._xor(block, previous))
            ciphertext += result
            previous = self._xor(block, result)
        return iv + ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % AES.block_size != 0:
            ciphertext = self._pad(ciphertext)
        plaintext = b''
        previous, ciphertext = ciphertext[:AES.block_size], ciphertext[AES.block_size:]
        for i in range(0, len(ciphertext), AES.block_size):
            block = ciphertext[i:i+AES.block_size]
            result = self._xor(self._cipher.decrypt(block), previous)
            plaintext += result
            previous = self._xor(block, result)
        return self._unpad(plaintext)

    def _pad(self, text):
        char = AES.block_size - len(text) % AES.block_size
        return text + bytes([char]) * char

    def _unpad(self, text):
        if len(text) == 0:
            return text
        return text[:-text[-1]]

    def _xor(self, data1, data2):
        return bytes(x^y for x, y in zip(data1, data2))
