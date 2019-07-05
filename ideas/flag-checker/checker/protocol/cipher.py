#!/usr/bin/python3

from base64 import b64encode, b64decode

from . import params
from .dh import DH
from .rsa import RSA, RSAEncryptor
from .utils import next_prime


class Cipher(object):
    CHECK = b'=CHECK='

    def __init__(self, io, params=params):
        self._rsa = self._init_rsa(params, io)

    def encrypt(self, text):
        text = Cipher.CHECK + text
        return b64encode(self._rsa.encrypt(text))

    def decrypt(self, data):
        text = self._rsa.decrypt(b64decode(data))
        if not text.startswith(Cipher.CHECK):
            raise Exception('Failed check!')
        return text[len(Cipher.CHECK):]

    def _init_rsa(self, params, io):
        p = self._dh_init_key(params, io)
        q = self._dh_init_key(params, io)
        rsa = RSA(p, q, params.RSA.e)
        return RSAEncryptor(rsa)

    def _dh_init_key(self, params, io):
        dh = DH(params.DH.g, params.DH.p, params.DH.nbits)
        io.print(str(dh.get_public()).encode())
        other_public = int(io.input().decode())
        key = dh.get_key(other_public)
        return int(next_prime(key))
