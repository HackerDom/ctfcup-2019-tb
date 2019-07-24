#!/usr/bin/python3

from PIL import Image
from fastecdsa.curve import P224
from Crypto.Util.number import long_to_bytes, bytes_to_long


class Cipher(object):
    def __init__(self, key, curve):
        self._key = bytes_to_long(key)
        self._P, self._Q = self._get_points(curve)

    def crypt(self, text):
        block = self._generate_block(len(text))
        return self._xor(text, block)

    def _get_points(self, curve):
        P = curve.G
        Q = 31337 * P
        return P, Q

    def _generate_block(self, size):
        data = b''
        for number in self._expand_key(self._key):
            data += long_to_bytes(number)
            if len(data) >= size:
                break
        return data[:size]

    def _expand_key(self, key):
        while True:
            key = (key * self._P).x
            yield (key * self._Q).x

    def _xor(self, block1, block2):
        return bytes(x^y for x, y in zip(block1, block2))


def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read()


def write_file(filename, data):
    with open(filename, 'wb') as file:
        file.write(data)


def read_image(filename):
    img = Image.open(filename)
    assert img.width == img.height
    assert img.width < 512
    return read_file(filename)


def main():
    key = read_file('key.txt')
    flag = read_image('flag.png')
    cipher = Cipher(key, P224)
    write_file('flag.png.enc', cipher.crypt(flag))


if __name__ == '__main__':
    main()
