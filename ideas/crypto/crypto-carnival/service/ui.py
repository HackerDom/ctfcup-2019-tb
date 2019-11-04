#!/usr/bin/env python3


class UI(object):
    def __init__(self, ciphers, plaintext):
        self._ciphers = ciphers
        self._current_cipher = self._ciphers[0]
        self._ciphertext = self._current_cipher.encrypt(plaintext)

    def run(self):
        while True:
            cipher = self._ciphers[self._select_cipher()]
            plaintext = self._current_cipher.decrypt(self._ciphertext)
            self._ciphertext = cipher.encrypt(plaintext)
            self._current_cipher = cipher
            while True:
                action = self._select_action()
                if action == 0:
                    self._set_ciphertext()
                if action == 1:
                    self._set_plaintext()
                if action == 2:
                    self._show_ciphertext()
                if action == 3:
                    self._show_publickey()
                if action == 4:
                    break
                if action == 5:
                    return

    def _set_ciphertext(self):
        print('Please, input a ciphertext (in hex):')
        self._ciphertext = bytes.fromhex(input())

    def _set_plaintext(self):
        print('Please, input a plaintext (in hex):')
        plaintext = bytes.fromhex(input())
        self._ciphertext = self._current_cipher.encrypt(plaintext)

    def _show_ciphertext(self):
        print('Your ciphertext (in hex):')
        print(self._ciphertext.hex())

    def _show_publickey(self):
        print('Your publickey:')
        print(self._current_cipher.publickey)

    def _select_action(self):
        return self._select('Please, select an action:', [
            'Set ciphertext',
            'Set plaintext',
            'Show ciphertext',
            'Show public key',
            'Select another cipher',
            'Exit'
        ])

    def _select_cipher(self):
        names = [cipher.__class__.__name__ for cipher in self._ciphers]
        return self._select('Please, select a cipher:', names)

    def _select(self, question, options):
        while True:
            print(f'[?] {question}')
            for i, option in enumerate(options):
                print(f'[{i+1}] {option}')
            choice = input()
            try:
                choice = int(choice)
            except ValueError:
                print('[-] Please, input an integer!')
                continue
            if not 1 <= choice <= len(options):
                print('[-] Please, select an option!')
                continue
            return choice - 1
