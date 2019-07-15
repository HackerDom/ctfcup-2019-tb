#!/usr/bin/python3

import re

from z3 import *
from string import printable


def build_alphabet(pattern):
    regex = re.compile(pattern)
    return ''.join(x for x in printable if regex.match(x))


def generate_bitvecs(name, length, size=8):
    names = [name + str(i) for i in range(length)]
    return BitVecs(' '.join(names), size)


def make_solution(ciphertext, pt_length, key_length, constraint):
    pt_vars = generate_bitvecs('pt', pt_length)
    key_vars = generate_bitvecs('key', key_length)
    equations = [pt_vars[0] == constraint]
    for i, ct in enumerate(ciphertext):
        equation = pt_vars[i % pt_length] ^ key_vars[i % key_length] == ct
        equations.append(equation)
    solver = Solver()
    solver.add(equations)
    if solver.check().r == -1:
        return None
    model = solver.model()
    return bytes(model[pt].as_long() for pt in pt_vars)


def brute_constraint(pattern, ciphertext, pt_length, key_length):
    alphabet = build_alphabet(pattern)
    for x in alphabet:
        solution = make_solution(ciphertext, pt_length, key_length, ord(x))
        if solution is not None:
            if re.match(pattern.encode(), solution):
                yield solution


def main():
    pattern = r'^\w+$'
    ciphertext = bytes.fromhex('7e03510aa168bc9d862fd5250151819c753e34b0c4b8011908fd3c64494b28570c5ea139e89fd479d8705304dece703261b5ccb2501a08a96c691e492f51035df769ecc980248c700250')
    pt_length = len(ciphertext) // 2
    max_key_length = 32
    for key_length in range(1, max_key_length + 1):
        print('key_length = {0}'.format(key_length))
        for solution in brute_constraint(pattern, ciphertext, pt_length, key_length):
            print('CTFCup{{{0}}}'.format(solution.decode()))


if __name__ == '__main__':
    main()
