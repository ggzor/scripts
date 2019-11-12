#!/usr/local/bin/python3.7

from sys import stdin
from pynput.keyboard import Controller
from re import compile
from sys import argv
from datetime import timedelta
from time import sleep

defaults = {
  'await': 0,
  'awaitPerLine': 0,
}
argument_pattern = compile(r'^--([^=]+)=(.+)$')

if __name__ == "__main__":
    args = defaults  

    for m in map(argument_pattern.match, argv):
        if m:
            args[m[1]] = m[2]

    if 'await' in args:
        sleep(float(args['await']))

    controller = Controller()

    for line in stdin:
        controller.type(line)
        sleep(float(args['awaitPerLine']))
