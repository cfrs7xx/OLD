__author__ = 'khanta'

import subprocess

def searchfiles(filename):
    error = ''
    output = ''

    with open('c:\\temp\\query.txt','r') as f:
        for line in f:
            line = line.rstrip() # remove trailing whitespace such as '\n'
            output = subprocess.call(['c:\\tools\\grep.exe', line, filename])

    return True, error
