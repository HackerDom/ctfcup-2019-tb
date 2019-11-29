#!/usr/bin/env python3

from ast import literal_eval
from models import Person, Oracle, Architect


class UI(object):
    def __init__(self, flag, bits, hackers, difficulty, lifes_count):
        self._flag = flag
        self._bits = bits
        self._hackers = hackers
        self._difficulty = difficulty
        self._lifes_count = lifes_count
        self._person = Person(self._bits)
        self._identity = self._person.identity
        self._oracle, self._architect = None, None

    def run(self):
        print(f'[+] Your identity: {self._identity}')
        while True:
            choice = self._wakeup_menu()
            if choice == 0:
                self._change_name()
                self._wakeup()
            if choice == 1:
                break

    def _main_menu(self):
        return self._select('Please, select an action:', [
            'Show your info',
            'Change your name',
            'Ask The Oracle',
            'Fight The Architect',
            'Forget'
        ])

    def _wakeup_menu(self):
        return self._select('Welcome to The Matrix!', [
            'Wake up',
            'Exit'
        ])

    def _wakeup(self):
        while True:
            choice = self._main_menu()
            if choice == 0:
                print(f'Name: {self._person.name}')
                print(f'Sign: {self._person.sign}')
            if choice == 1:
                self._change_name()
            if choice == 2:
                if not (self._oracle or self._spawn_oracle()):
                    print('[-] The Oracle is not available for you!')
                    continue
                print(f'The Oracle says: {self._oracle.ask()}')
            if choice == 3:
                if not (self._architect or self._spawn_architect()):
                    print('[-] The Architect is not available for you!')
                    continue
                self._fight()
                print('[!] But it was just a dream...')
                break
            if choice == 4:
                self._oracle, self._architect = None, None
                break

    def _change_name(self):
        while True:
            print('[?] Please, enter your name:')
            name = input()
            if name.lower() in self._hackers:
                choice = self._select('It is not you! Do you want to verify your identity?', [
                    'Yes',
                    'No'
                ])
                if choice == 0:
                    print('[?] Please, enter your signature:')
                    sign = literal_eval(input())
                    if self._person.verify_sign(name, sign):
                        self._person.change_name(name, sign)
                        break
                    else:
                        print('[-] Wrong signature!')
                        continue
                continue
            self._person.set_name(name)
            break

    def _fight(self):
        life = self._lifes_count
        while life > 0:
            print(f'[!] Life: {life}')
            question = self._oracle.ask()
            print('[+] Question asked.')
            print('[?] Please, input an answer:')
            actual = literal_eval(input())
            expected = self._architect.answer(question)
            if actual == expected:
                print(f'[+] You win! Here is the flag: {self._flag}')
                return
            print(f'[-] You are wrong! Correct answer is: {expected}')
            life -= 1
        print('[-] You lose!')

    def _spawn_oracle(self):
        if self._person.name not in self._hackers:
            return False
        self._oracle = Oracle(sum(self._identity))
        return True

    def _spawn_architect(self):
        if not (self._oracle or self._spawn_oracle()):
            return False
        if self._person.name not in self._hackers:
            return False
        self._architect = Architect(self._bits, self._difficulty)
        return True

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
