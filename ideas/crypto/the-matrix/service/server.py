#!/usr/bin/env python3

from ui import UI


def main(flag):
    bits = 1024
    hackers = ['neo', 'trinity', 'morpheus']
    difficulty = 10
    lifes_count = 3
    ui = UI(flag, bits, hackers, difficulty, lifes_count)
    ui.run()


if __name__ == '__main__':
    with open('flag.txt', 'r') as file:
        flag = file.read()
    try:
        main(flag)
    except Exception as e:
        print(e)
