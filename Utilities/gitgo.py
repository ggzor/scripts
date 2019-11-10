#!/usr/bin/env python3

import colorama
colorama.init()

from subprocess import run
from colorama import Fore, Style
from sys import argv

def withColor(color, content):
    return f'{color}{content}{Style.RESET_ALL}'

def runCommand(command):
    return run(command.split(' '), capture_output=True).stdout.decode('utf-8').strip()

if __name__ == '__main__':
    command = argv[1]

    if command == 'ls':
        fileName = argv[2] if len(argv) > 2 else ''
    elif command == 'to':
        fileName = argv[3] if len(argv) > 3 else ''
    
    if fileName != '':
        fileName = ' ' + fileName

    output = runCommand(f'git log --all --pretty=oneline{fileName}')

    if output == "":
        print(withColor(Fore.RED, "The file is not being tracked."))
        exit(-1)

    destinations = [s.split(' ', 1) for s in output.split('\n')]
    currentCommit = runCommand('git rev-parse HEAD')

    if command == 'ls':
        for i, (h, d) in enumerate(destinations):
            isCurrentCommit = currentCommit == h 
            print(withColor(Fore.GREEN, f'{"✓" if isCurrentCommit else " "} {i}    '), end='')
            print(withColor(Fore.YELLOW, f'{h[:7]}    '), end='')
            print(d)

    if command == 'to':
        index = int(argv[2])

        if 0 <= index < len(destinations):
            d = destinations[index]
            runCommand(f'git checkout {d[0]}')
            print(f'Switched to {withColor(Fore.GREEN, index)} {withColor(Fore.YELLOW, d[0][:7])} {d[1]}')
        else:
            print(withColor(Fore.RED, f'Invalid index: {index}'))


