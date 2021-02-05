#!/usr/bin/env python
import sys

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        print(eval(arg))
else:
    print(eval(sys.stdin.read()))
