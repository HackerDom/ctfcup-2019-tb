#!/usr/bin/env python3

from os import urandom


class Architect(object):
    def __init__(self, bits, strength):
        self._bits = bits
        self._computers = [self._rand(bits) for _ in range(strength)]

    def answer(self, question):
        value = 0
        length = len(self._computers)
        for i, computer in enumerate(self._computers):
            value += computer * (question ** (length - i - 1))
        return value

    def _rand(self, bits):
        return int.from_bytes(urandom(bits // 8), 'big')
