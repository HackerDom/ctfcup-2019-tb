#!/usr/bin/env sage

import sys


def find_ABC(point, value):
    x, y = point.xy()
    A = (8 * (value + 3) - x + y) / (2 * (4 - x) * (value + 3))
    B = (8 * (value + 3) - x - y) / (2 * (4 - x) * (value + 3))
    C = (-4 * (value + 3) - (value + 2) * x) / ((4 - x) * (value + 3))
    d = lcm(map(denominator, (A, B, C)))
    return d * A, d * B, d * C


def check_ABC(A, B, C):
    return A > 0 and B > 0 and C > 0


def main():
    value = 16
    p, q = 4 * value * value + 12 * value - 3, 32 * (value + 3)
    curve = EllipticCurve([0, p, 0, q, 0])
    sys.stderr.write('curve: ' + str(curve) + '\n')
    G = curve.gen(0)
    sys.stderr.write('G: ' + str(G) + '\n')
    m = 1
    while True:
        sys.stderr.write('m: ' + str(m) + '\n')
        A, B, C = find_ABC(m * G, value)
        sys.stderr.write('A, B, C: ' + str((A, B, C)) + '\n')
        if check_ABC(A, B, C):
            break
        m += 1
    sys.stdout.write('\n'.join(map(str, (A, B, C))))


if __name__ == '__main__':
    main()
