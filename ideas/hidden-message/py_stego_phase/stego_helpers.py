# -*- coding: utf-8 -*-

__author__ = 'Ilya Shoshin (Galarius)'
__copyright__ = 'Copyright 2015, Ilya Shoshin (Galarius)'

from math import atan2, floor
import numpy as np

def chunks(l, n):
    """
    Split list into chunks.
    source: http://stackoverflow.com/a/1751478

    :param l: list to split
    :param n: chunk size
    :return: [[],[],[],...]
    """
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def arg(z):
    """
    Argument of a complex number
    :param z: complex number
    :return:  arg(z)
    """
    return atan2(z.imag, z.real)


def vec_2_str(vec):
    """
    Convert vector of integers to string.
    :param vec: [int, int, ...]
    :return: string
    """
    char_vec = [chr(i) for i in vec]
    return ''.join(char_vec)


def str_2_vec(str):
    """
    Convert vector of integers to string.
    :param str: string
    :return:    [int, int, int, ...]
    """
    return [ord(i) for i in str]


def d_2_b(x, size=8):
    """
    Convert decimal to byte list
    :param x:    decimal
    :param size: the size of byte list
    :return: e.g. [0, 0, 1, ...]
    """
    s = np.sign(x)
    v = size * [None]
    for i in range(0, size):
        v[i] = abs(x) % 2
        x = int(floor(abs(x)/2.0))
    return s * v


def b_2_d(x):
    """
    Convert byte list to decimal
    :param x:   byte list
    :return:    decimal
    """
    s = 0
    for i in range(0, len(x)):
        s += x[i]*2**i
    return s