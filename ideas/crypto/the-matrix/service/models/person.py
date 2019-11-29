#!/usr/bin/env python3

from os import urandom
from Crypto.PublicKey import DSA


class Person(object):
    def __init__(self, bits):
        self._dsa = DSA.generate(bits)
        self._name = None
        self._sign = None

    @property
    def identity(self):
        return (
            self._dsa.key.p,
            self._dsa.key.q,
            self._dsa.key.g,
            self._dsa.key.y
        )

    @property
    def name(self):
        return self._name

    @property
    def sign(self):
        return self._sign

    def set_name(self, name):
        self._name = name
        self._sign = self._make_sign(self._name)

    def change_name(self, name, sign):
        if not self.verify_sign(name, sign):
            raise Exception('wrong signature')
        self._name = name
        self._sign = sign

    def verify_sign(self, name, sign):
        return self._dsa.verify(self._toint(name), sign)

    def _make_sign(self, name):
        k = self._rand(self._dsa.key.q.bit_length() - 1)
        return self._dsa.sign(self._toint(name), k)

    def _toint(self, data):
        return int.from_bytes(data.encode(), 'big')
    
    def _rand(self, bits):
        return int.from_bytes(urandom(bits // 8), 'big')
