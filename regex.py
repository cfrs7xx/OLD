__author__ = 'khanta'

import re




def SearchFiles(pattern, filename):
    status = True
    error = ''
    asciistrings = []

    chars = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
    shortest_run = 4

    regexp = '[%s]{%d,}' % (chars, shortest_run)

    charpattern = re.compile(regexp)
    pattern = b'[a-f]+\d+'

    with open(filename, 'rb') as f:
        filedata = f.read()
        strings = charpattern.findall(filedata)
        print(strings)
    return status, error

