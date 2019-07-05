#!/usr/bin/python3

from gmpy2 import invert, next_prime
from random import randint


def randbits(nbits):
    lower = 1 << (nbits - 1)
    upper = (1 << nbits) - 1
    return randint(lower, upper)

def make_prime(nbits):
    return int(next_prime(randbits(nbits)))

def long_to_bytes(n):
    bitlen = n.bit_length()
    nbits = (bitlen + 7) >> 3
    return n.to_bytes(nbits, 'little')

def bytes_to_long(b):
    return int.from_bytes(b, 'little')
