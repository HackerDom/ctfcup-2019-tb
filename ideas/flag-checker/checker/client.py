#!/usr/bin/python3

import socket

from protocol.io import SocketIO, EncryptedIO


def make_socket(host, port, timeout=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))
    return sock


def main():
    host, port = '0.0.0.0', 3307
    sock = make_socket(host, port)

    io = SocketIO(sock)
    io = EncryptedIO(io)
    
    print(io.input().decode())
    io.print(input().encode())
    print(io.input().decode())
    print(io.input().decode())
    print(io.input().decode())
    
    sock.close()


if __name__ == '__main__':
    main()
