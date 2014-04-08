__author__ = 'khanta'
__author__ = 'tschlein'
#Calls all the main applications
#Prints headers and footers
#Bulk Path must not exist if so, it removes EVERYTHING

import sys
import os
import argparse
import datetime
import be
import shutil
import regex
import HTML
import hashing
import search
import UnzipFile
#from hashing import hashRecursive
from sys import platform as _platform
import HTMLWriter

verbosity = 0
debug = 0

def IdentifyFile(filename):
    status = True
    error = ''
    filetype = ''

    #try:
    if debug >= 1:
        print('Entering IdentifyFile')
    if debug >= 2:
        print('\tFile passed in: ' + str(filename))
    ext = os.path.splitext(filename)[-1].lower()
    with open(filename, "rb") as f:
        header = f.read(4)
        if ext == '.apk' and header == b'\x50\x4B\x03\x04':
            if debug >= 2:
                print('\tFiletype: APK.')
            filetype = 'apk'
        elif ext == '.ipa' and header == b'\x50\x4B\x03\x04':
            if debug >= 2:
                print('\tFiletype: IPA.')
            filetype = 'ipa'
    return filetype, status, error

def Failed(error):
    print('  * Error: ' + str(error))
    print('+--------------------------------------------------------------------------+')
    print('| Failed.                                                                  |')
    print('+--------------------------------------------------------------------------+')
    sys.exit(1)

def Header(outputpath, file):
    print('')
    print('+--------------------------------------------------------------------------+')
    print('|Mobile Application and Analysis Framework                                 |')
    print('+---------------------------------------------------------------------------')
    print('|Authors: Tahir Khan - tkhan9@gmu.edu / Tim Schleining - tschlein@gmu.edu  |')
    print('+--------------------------------------------------------------------------+')
    print('  Date Run: ' + str(datetime.datetime.now()))
    print('+--------------------------------------------------------------------------+')
    print('  Input File:   ' + str(file))
    print('  Output Path:  ' + str(outputpath))
    print('+--------------------------------------------------------------------------+')

def Completed():
    print('| [*] Completed.                                                           |')
    print('+--------------------------------------------------------------------------+')
    sys.exit(0)


def main(argv):
    #try:
        global verbosity
        config = '.\paths.ini'
        #parse the command-line arguments
        parser = argparse.ArgumentParser(description="Main program for MAFA.", add_help=True)
        parser.add_argument('-p', '--path', help='The output path for files.', required=True)
        parser.add_argument('-f', '--filename', help='The file to ingest.', required=True)
        parser.add_argument('-v', '--verbose', help='The level of debugging.', required=False)
        parser.add_argument('-c', '--config', help='The config file to use.', required=False)
        parser.add_argument('--version', action='version', version='%(prog)s 1.5')
        args = parser.parse_args()
        if args.path:
            path = args.path
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                shutil.rmtree(path)
        if args.filename:
            filename = args.filename
        if args.config:
            config == args.config
        if args.verbose:
            verbosity = args.verbose
            verbosity = int(verbosity)
        if _platform == "linux" or _platform == "linux2":
            oper = 'Linux'
        elif _platform == "darwin":
            oper = 'Mac'
        elif _platform == "win32":
            oper = 'Windows'
        if debug >= 1:
            print('Entered main:')
            print('\tOperating System: ' + str(oper))
            print('\tDebug Level: ' + str(debug))
            #if (os == 'Windows'):
            #    print ('Error: System not supported.')
            #    sys.exit(1)
        Header(path, filename)

        fileype, status, error = IdentifyFile(filename)
        if status:
            print('| [+] File Identified.                                                     |')
        else:
            print('| [-] File Identified.                                                     |')
            Failed(error)
        status, error = hashing.hashFile(filename, verbosity)
        if status:
            print('| [+] Hashing File.                                                        |')
        else:
            print('| [-] Hashing File.                                                        |')
            Failed(error)
        status, error = UnzipFile.Unzip(filename, path)
        if status:
            print('| [+] File Unzipped.                                                       |')
        else:
            print('| [-] File Unzipped.                                                       |')
            Failed(error)
        #status, error = be.be_call(filename, 'c:\\temp\\bulk', oper)
        if status:
            print('| [+] Bulk Extractor Executed.                                             |')
        else:
            print('| [-] Bulk Extractor Executed.                                             |')
            Failed(error)
        status, error = hashing.hashRecursive(path, verbosity)
        if status:
            print('| [+] Hashing Files.                                                       |')
        else:
            print('| [-] Hashing Files.                                                       |')
            Failed(error)

        status, error = search.grepsearch('C:\\Users\\khanta\\Dropbox\\Git\\MAFA\\paths.ini', filename, path)
        if status:
            print('| [+] Searching Files        .                                             |')
        else:
            print('| [-] Searching Files        .                                             |')
            Failed(error)
        HTMLWriter.test()
        Completed()


    #except:
        #sys.exit(0)


main(sys.argv[1:])
