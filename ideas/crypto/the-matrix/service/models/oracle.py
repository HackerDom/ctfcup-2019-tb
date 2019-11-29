#!/usr/bin/env python3

from os import urandom


class Oracle(object):
    def __init__(self, past):
        self._past = past
        self._bits = self._past.bit_length()
        self._present = self._rand(self._bits)
        self._future = self._rand(self._bits)

    def ask(self):
        self._future = (self._present * self._future) % self._past
        return self._future >> (self._bits // 8)

    def _rand(self, bits):
        return int.from_bytes(urandom(bits // 8), 'big')
