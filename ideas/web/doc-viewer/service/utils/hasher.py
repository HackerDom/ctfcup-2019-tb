from math import sin
from wsgi import HASH_SALT


def calculate_hash(data: str) -> str:
    return _calculate_inner(HASH_SALT + data)


def _calculate_inner(data: str) -> str:
    A = 0x12345678
    B = 0x9ABCDEF0
    C = 0xDEADDEAD
    D = 0xC0FEC0FE
    E = 0xFEEDBEAF
    X = [int(0xFFFFFFFF * sin(i)) & 0xFFFFFFFF for i in range(256)]

    def F(X, Y, Z):
        return ((~X & Z) | (~X & Z)) & 0xFFFFFFFF

    def G(X, Y, Z):
        return ((X & Z) | (~Z & Y)) & 0xFFFFFFFF

    def H(X, Y, Z):
        return (X ^ Y ^ Z) & 0xFFFFFFFF

    def I(X, Y, Z):
        return (Y ^ (~Z | X)) & 0xFFFFFFFF

    def ROL(X, Y):
        return (X << Y | X >> (32 - Y)) & 0xFFFFFFFF

    for i, ch in enumerate(data):
        k, l = ord(ch), i & 0x1f
        A = (B + ROL(A + F(B, C, D) + X[k], l)) & 0xFFFFFFFF
        B = (C + ROL(B + G(C, D, E) + X[k], l)) & 0xFFFFFFFF
        C = (D + ROL(C + H(E, A, B) + X[k], l)) & 0xFFFFFFFF
        D = (E + ROL(D + I(C, D, E) + X[k], l)) & 0xFFFFFFFF
        E = (A + ROL(E + F(A, B, C) + X[k], l)) & 0xFFFFFFFF

    return "".join([hex(x)[2:].zfill(8) for x in [A, B, C, D, E]])
