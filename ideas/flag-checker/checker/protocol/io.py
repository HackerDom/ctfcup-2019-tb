#!/usr/bin/python3

import sys

from .cipher import Cipher


class BaseIO(object):
    def __init__(self):
        pass

    def input(self):
        raise NotImplementedError()

    def print(self, text):
        raise NotImplementedError()


class SimpleIO(BaseIO):
    def __init__(self):
        pass

    def input(self):
        sys.stdin.buffer.flush()
        return sys.stdin.buffer.readline()[:-1]

    def print(self, text):
        sys.stdout.buffer.write(text + b'\n')
        sys.stdout.buffer.flush()


class SocketIO(BaseIO):
    def __init__(self, socket):
        self._socket = socket
        self._file = socket.makefile()

    def input(self):
        self._file.buffer.flush()
        return self._file.buffer.readline()[:-1]

    def print(self, data):
        self._socket.send(data + b'\n')


class EncryptedIO(BaseIO):
    def __init__(self, io):
        self._io = io
        self._cipher = Cipher(self._io)

    def input(self):
        data = self._io.input()
        return self._cipher.decrypt(data)

    def print(self, text):
        data = self._cipher.encrypt(text)
        self._io.print(data)
