#!/usr/bin/env python3

import pexpect
import subprocess
from sys import argv

def saveFile(inputs):
    print("Name of record file: ", end='')

    try:
        with open(input(), 'w') as f:
            f.write('\n'.join(inputs) + '\n')
    except KeyboardInterrupt:
        print('\nYou decided not to save the file, here are the inputs if you regret: ')
        print('\n'.join(inputs) + '\n')
    except OSError as ex:
        print(ex)
        print('It was not possible to open the file, here are the inputs: ')
        print('\n'.join(inputs) + '\n')

if __name__ == '__main__':
    if len(argv) > 1:
        options = argv[1:]
        
        command = pexpect.spawn(' '.join(options))
        command.setecho(False)

        inputs = []

        # Expect input before any input
        if command.isalive():
            command.expect('.+')

        while True:
            try:
                if command.isalive():
                    userInput = input()
                    command.sendline(userInput)
                    command.expect('.+')
                    print(command.after.decode('utf-8'), end='')

                    inputs.append(userInput)
                else:
                    raise EOFError
            except EOFError:
                command.sendeof()
                break
            except Exception as ex:
                print('A unexpected error has ocurred: ')
                print(ex)
                saveFile(inputs)
                exit(-1)

        saveFile(inputs)
