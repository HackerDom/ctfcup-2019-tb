from socket import *
from math import sin

HOST = "192.168.56.4"
PORT = 4331

def calculate_hash(hash: str, data: str, prev_data_length: int) -> str:
    hash_bytes = bytes.fromhex(hash)
    A = int.from_bytes(hash_bytes[0:4], byteorder="big")
    B = int.from_bytes(hash_bytes[4:8], byteorder="big")
    C = int.from_bytes(hash_bytes[8:12], byteorder="big")
    D = int.from_bytes(hash_bytes[12:16], byteorder="big")
    E = int.from_bytes(hash_bytes[16:20], byteorder="big")
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
        k, l = ord(ch), (i + prev_data_length) & 0x1f
        A = (B + ROL(A + F(B, C, D) + X[k], l)) & 0xFFFFFFFF
        B = (C + ROL(B + G(C, D, E) + X[k], l)) & 0xFFFFFFFF
        C = (D + ROL(C + H(E, A, B) + X[k], l)) & 0xFFFFFFFF
        D = (E + ROL(D + I(C, D, E) + X[k], l)) & 0xFFFFFFFF
        E = (A + ROL(E + F(A, B, C) + X[k], l)) & 0xFFFFFFFF

    return "".join([hex(x)[2:].zfill(8) for x in [A, B, C, D, E]])

def recv(sock):
    data = b""

    while True:
        try:
            a = sock.recv(1024)
            if not a:
                break
            data += a
        except:
            break

    return data

def send_command(command):
    sock = socket()
    sock.settimeout(2)
    sock.connect((HOST, PORT))
    recv(sock)
    sock.send((command + "\n").encode())
    data = recv(sock).decode()[:-1]
    return data

user_name = "leo5"
hash = send_command("m_reg a_login={0}".format(user_name))
print(hash)
append_data = "admin"
new_hash = calculate_hash(hash, append_data, len(user_name))
flag = send_command("m_flag a_login={2}{0} u_{1}".format(append_data, new_hash, user_name))
print(flag)
