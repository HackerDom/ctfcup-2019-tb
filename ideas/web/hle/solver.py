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

user_name = "123"
hash = "4793cd3b570132d23bee26af8d604b6c94eb583a"
print(hash)
append_data = "admin"
new_hash = calculate_hash(hash, append_data, len(user_name))
print(user_name + append_data, new_hash)
