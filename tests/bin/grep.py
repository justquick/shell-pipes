#!/usr/bin/env python
import re
import sys
import os


def line_matcher(lines):
    for line in lines:
        if re.match(sys.argv[1], line):
            print(line, end='')


if not sys.argv[2:]:
    line_matcher(sys.stdin.readlines())
else:
    for f in filter(os.path.isfile, sys.argv[2:]):
        line_matcher(open(f).readlines())
