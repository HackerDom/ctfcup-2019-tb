#!/usr/bin/python3

import struct

from .utils import invert, long_to_bytes, bytes_to_long


class RSAEncryptor(object):
    def __init__(self, rsa):
        self._rsa = rsa
        self._maxlen = (rsa.key_length() - 1) // 8
        self._serializer = RSASerializer()

    def encrypt(self, pt):
        ms = self._split_pt(pt)
        cs = map(self._rsa.encrypt, ms)
        return self._serializer.serialize(cs)

    def decrypt(self, ct):
        cs = self._serializer.deserialize(ct)
        ms = map(self._rsa.decrypt, cs)
        return self._join_pt(ms)

    def _split_pt(self, pt):
        ms = []
        for i in range(0, len(pt), self._maxlen):
            part = pt[i:i+self._maxlen]
            ms.append(bytes_to_long(part))
        return ms

    def _join_pt(self, ms):
        pt = b''
        for m in ms:
            pt += long_to_bytes(m)
        return pt


class RSASerializer(object):
    def serialize(self, cs):
        ct = b''
        for c in cs:
            part = long_to_bytes(c)
            fmt = '<I%ds' % len(part)
            ct += struct.pack(fmt, len(part), part)
        return ct

    def deserialize(self, ct):
        i = 0
        cs = []
        while i < len(ct):
            length = struct.unpack('<I', ct[i:i+4])[0]
            i += 4
            part = struct.unpack('%ds' % length, ct[i:i+length])[0]
            cs.append(bytes_to_long(part))
            i += length
        return cs


class RSA(object):
    def __init__(self, p, q, e):
        self._n = p * q
        self._e = e
        self._d = self._compute_d(p, q, e)

    def key_length(self):
        return self._n.bit_length()

    def encrypt(self, m):
        return pow(m, self._e, self._n)

    def decrypt(self, c):
        return pow(c, self._d, self._n)

    def _compute_d(self, p, q, e):
        phi = (p - 1) * (q - 1)
        return int(invert(e, phi))
