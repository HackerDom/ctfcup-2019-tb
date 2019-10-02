#!/usr/bin/env python3

import socket
import params

from argparse import ArgumentParser
from protocol import IO, NoEncryption, RSAEncryption
from subprocess import Popen, PIPE


# ============================================
# CLIENT SIDE IMPLEMENTATION IS NOT VULNERABLE
#        THIS IS A CRYPTO CHALLENGE, SO       
# PLEASE DON'T DIVE INTO SOCKETS AND PROCESSES
# ============================================ 


def parse_args():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--local', action='store_true', help='run server locally')
    group.add_argument('--host', help='server address')
    parser.add_argument('--port', type=int, help='server port')
    parser.add_argument('--cipher', type=int, choices=[0, 1], default=1, help='cipher type (No=0, RSA=1)')
    args = parser.parse_args()
    if args.host and not args.port:
        parser.error('argument --host: argument --port is required')
    return args


def make_process():
    return Popen(['python3', 'server.py'], stdin=PIPE, stdout=PIPE)


def make_socket(host, port, timeout=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))
    return sock


def interact(io, cipher_type):
    for i in range(3):
        io.read()
    io.write(str(cipher_type))
    if cipher_type == 0:
        cipher = NoEncryption()
    elif cipher_type == 1:
        cipher = RSAEncryption(io, params)
    print(cipher.decrypt(io.read()))
    flag = input()
    io.write(cipher.encrypt(flag))
    for i in range(3):
        print(cipher.decrypt(io.read()))


def main():
    args = parse_args()
    if args.local:
        process = make_process()
        io = IO(process.stdout, process.stdin)
    else:
        sock = make_socket(args.host, args.port)
        io = IO(sock.makefile('rb'), sock.makefile('wb'))
    interact(io, args.cipher)
    if args.local:
        process.kill()
    else:
        sock.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('[-] %s' % e)
