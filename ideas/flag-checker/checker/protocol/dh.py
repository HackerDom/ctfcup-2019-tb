#!/usr/bin/python3

from .utils import make_prime


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
