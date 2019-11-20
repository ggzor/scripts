#!/usr/local/bin/python3.7

import argparse
import functools
import numpy

from pynput.keyboard import Controller, Listener, Key, KeyCode
from sys import stdin
from time import sleep

def timed_typing(args):
    controller = Controller()
    sleep(args.before_await)

    for line in stdin:
        controller.type(line)
        sleep(args.line_await)

def user_input_typing(args):
    def waitKeys(key_groups):
        pressed_keys = set()
        all_required_keys = functools.reduce(frozenset.union, key_groups)
    
        def on_press(key):
            if key in all_required_keys:
                pressed_keys.add(key)
            
            if pressed_keys in key_groups:
                return False

        def on_release(key):
            if key in pressed_keys:
                pressed_keys.remove(key)

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        return pressed_keys

    if waitKeys([args.begin_key, args.stop_key]) == args.stop_key:
        print('Typing was stopped.')
        exit(0)

    # Strangely, required 
    sleep(args.before_await)

    controller = Controller()

    first = True
    for line in stdin:
        if not first and args.pause:
            key_group = waitKeys([args.begin_key, args.next_key, args.stop_key])
            if key_group == args.begin_key:
                args.pause = False
            elif key_group == args.stop_key:
                print('Typing was stopped.')
                exit(0)

        # Hacky, but required to let the characters be typed
        if not first:
            sleep(args.char_await * len(prevline))
        prevline = line

        first = False

        controller.type(line)
        sleep(args.line_await)

def parse_keys(keys):
    def map_key(k):
        k = k.upper()

        modifiers = {
            'CTRL': Key.ctrl,
            'SHIFT': Key.shift,
            'ALT': Key.alt
        }

        if len(k) == 1 and k.isalpha():
            return KeyCode.from_char(k)
        else:
            if k in modifiers:
                return modifiers[k]
            else:
                raise argparse.ArgumentTypeError(f'The key "{k}" was not recognized')

    if keys == '' or keys.isspace():
        raise argparse.ArgumentTypeError('The key cannot be empty')

    return frozenset(map(map_key, keys.split('+')))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Types the input that is provided via stdin.')

    parser.add_argument('-l', '--line-await',
                        metavar='LINE_AWAIT',
                        help='Time to await between each line',
                        type=float, dest='line_await', default=0.2)

    parser.add_argument('-c', '--char-await',
                        metavar='CHAR_AWAIT',
                        help='Time to await for each character',
                        type=float, dest='char_await', default=0.01)

    subparser = parser.add_subparsers()

    timed = subparser.add_parser('timed', aliases=['t'], help='Uses timers to delay the typing')

    timed.add_argument('-a', '--await',
                        metavar='AWAIT',
                        help='Time to await before starting to write',
                        type=float, dest='before_await', default=3)
    
    timed.set_defaults(func=timed_typing)

    user_input = subparser.add_parser('input', aliases=['i'], help='Waits for user input to trigger typing')

    user_input_main_options = user_input.add_argument_group(title='main options')

    user_input_main_options.add_argument('-p', '--pause', 
                            help='Pauses the typing for each line, see --next-key and --stop-key',
                            dest='pause', action='store_true')

    user_input_main_options.add_argument('-a', '--await',
                                         metavar='AWAIT',
                                         help=('Time to await before starting to write, you will rarely have to change'
                                               ' unless you have problems with line feeds'),
                                         type=float, dest='before_await', default=0.3)

    user_input_shortcuts = user_input.add_argument_group(title='shortcuts')
    user_input_shortcuts.add_argument('-k', '--begin-key',
                            metavar='<kc>',
                            help='The key combination to start typing or continue the typing if "pause" is specified (by default, Ctrl+Alt+Shift+R)',
                            dest='begin_key', default='Ctrl+Alt+Shift+R', type=parse_keys)

    user_input_shortcuts.add_argument('-n', '--next-key',
                            metavar='<kc>',
                            help='The key combination to type the next line (by default, Ctrl+Alt+Shift+N)',
                            dest='next_key', default='Ctrl+Alt+Shift+N', type=parse_keys)

    user_input_shortcuts.add_argument('-s', '--stop-key',
                            metavar='<kc>',
                            help='The key combination to stop typing (by default, Ctrl+Alt+Shift+S)',
                            dest='stop_key', default='Ctrl+Alt+Shift+S', type=parse_keys)

    user_input.set_defaults(func=user_input_typing)

    args = parser.parse_args()
    args.func(args)
