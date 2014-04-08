__author__ = 'khanta'

debug = 2

import sys
import os
import zipfile

def Unzip(file, outputpath):
    if debug >= 1:
        print('Entering Unzip.')
    if debug >= 2:
        print('\tFilename passed in: ' + str(file))
        print('\tPath passed in: ' + str(outputpath))
    if debug >= 3:
        print('Zip Info:' + str(zipfile.ZipInfo(file)))
    with zipfile.ZipFile(file) as zf:
        zf.extractall(outputpath)
    return True, ''

