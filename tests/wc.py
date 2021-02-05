#!/usr/bin/env python
import sys


def count(content):
    lines = len(content.splitlines())
    words = len(content.split())
    chars = len(content)
    print('%d\t%d\t%d' % (lines, words, chars))


if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        count(open(arg).read())
else:
    count(sys.stdin.read())
