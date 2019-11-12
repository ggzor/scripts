#!/usr/bin/env python3

import pexpect
from sys import argv

if __name__ == '__main__':
    if len(argv) >= 3:
        try:
            p = pexpect.spawn(' '.join(argv[2:]))            
            with open(argv[1]) as f:
                for l in f.readlines():
                    p.sendline(l.strip('\n'))
                    p.expect('.+')
                    print(p.after.decode('utf-8'), end='')
                p.sendeof()
            p.wait()
        except EOFError:
            pass
