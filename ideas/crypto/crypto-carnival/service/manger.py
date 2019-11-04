#!/usr/bin/env python3

from decimal import Decimal, getcontext, ROUND_CEILING, ROUND_FLOOR
from hashlib import sha1
from ciphers.rsa import RSA


class Manger(object):
    def __init__(self, n, e, oracle):
        self._n, self._e, self._c = n, e, None
        self._size = (self._n.bit_length() + 7) // 8
        self._oracle = oracle
        self._B = Decimal(2) ** Decimal(8 * (self._size - 1))
        self.oracle_calls = 0
        assert 2 * self._B < self._n, "Shouldn't happen"

    def decrypt(self, c):
        self._c = c
        t1 = self._step1()
        t2 = self._step2(t1)
        t3 = self._step3(t2)
        return self._unpad(int(t3))
    
    def _call_oracle(self, f):
        f = int(f)
        h = pow(f, self._e, self._n)
        w = (h * self._c) % self._n
        self.oracle_calls += 1
        print(self.oracle_calls)
        return self._oracle(w)

    def _unpad(self, m):
        hlen = 20
        lhash = sha1(b'').digest()

        em = m.to_bytes(self._size, byteorder='big')

        maskedseed = em[1:1+hlen]
        maskeddb = em[1+hlen:]

        seedmask = RSA._expand(None, maskeddb, hlen)
        seed = RSA._xor(None, maskedseed, seedmask)
        dbmask = RSA._expand(None, seed, self._size - hlen - 1)
        db = RSA._xor(None, maskeddb, dbmask)

        _lhash = db[:hlen]

        assert _lhash == lhash, 'lhash should match _lhash'

        i = db.index(b'\x01')
        return db[i+1:]

    def _step1(self):
        f1 = 1
        while not self._call_oracle(f1):
            f1 = 2 * f1
        return f1

    def _step2(self, f1):
        f2 = (self._n + self._B) // self._B * (f1 // 2)
        while self._call_oracle(f2):
            f2 += f1 // 2
        return f2

    def _step3(self, f2):
        getcontext().prec = 500

        m_min = self._dec(Decimal(self._n) / f2, ROUND_CEILING)
        m_max = self._dec((self._n + self._B) / f2, ROUND_FLOOR)
        t_tmp = self._dec((2 * self._B) / (m_max - m_min), ROUND_FLOOR)
        i = self._dec((t_tmp * m_min) / self._n, ROUND_CEILING)
        f3 = self._dec((i * self._n) / m_min, ROUND_CEILING)

        while True:
            if not self._call_oracle(f3):
                m_max = self._dec((i*self._n + self._B) / f3, ROUND_FLOOR)
            else:
                m_min = self._dec((i*self._n + self._B) / f3, ROUND_CEILING)
            diff = Decimal(m_max - m_min)
            print(f'm_max - m_min: {diff}')
            if diff == 0:
                break
            t_tmp = self._dec((2 * self._B) / (m_max - m_min), ROUND_FLOOR)
            i = self._dec((t_tmp * m_min) / self._n, ROUND_CEILING)
            f3 = self._dec((i * self._n) / m_min, ROUND_CEILING)

        print(f'f3 - B: {f3 - self._B}')
        return m_min

    def _dec(self, thing, rounding):
        return Decimal(thing).to_integral_value(rounding)
