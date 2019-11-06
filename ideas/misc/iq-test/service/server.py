#!/usr/bin/env python3

from decimal import Decimal, getcontext


def center_line(line, length):
    return line.rjust((length + len(line)) // 2).ljust(length)


def build_banner(value):
    value = str(value)
    padding = ' ' * (len(value) + 3)
    lines = [
        '',
        '95% of people cannot solve this!',
        '',
        '  A       B       C  ' + padding,
        '⎯⎯⎯⎯⎯ + ⎯⎯⎯⎯⎯ + ⎯⎯⎯⎯⎯ = ' + value,
        'B + C   A + C   A + B' + padding,
        '',
        'Can you find positive integer values',
        'for A, B and C?',
        ''
    ]
    length = max(map(len, lines))
    banner = []
    banner.extend([
        '',
        ' ╔══' + '═' * length + '══╗ '
    ])
    banner.extend([
        ' ║  ' + center_line(line, length) + '  ║' for line in lines
    ])
    banner.extend([
        ' ╚══' + '═' * length + '══╝ ',
        ''
    ])
    return '\n'.join(banner)


def check(A, B, C, value):
    if sum(map(len, (A, B, C))) > 65536:
        return False
    A, B, C = map(Decimal, (A, B, C))
    if A <= 0 or B <= 0 or C <= 0:
        return False
    return A / (B + C) + B / (A + C) + C / (A + B) == value


def main(flag):
    value = 16
    print(build_banner(value))
    A = input('A = ')
    B = input('B = ')
    C = input('C = ')
    getcontext().prec = 31337
    if check(A, B, C, value):
        print(flag)
    else:
        print('No')


if __name__ == '__main__':
    with open('flag.txt', 'r') as file:
        flag = file.read()
    try:
        main(flag)
    except Exception as e:
        print(e)
