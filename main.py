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
import parsebe

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
    data = ''
    data += '+--------------------------------------------------------------------------+\n\r'
    data += ''
    data += 'Mobile Application and Analysis Framework\n\r'
    data += '+---------------------------------------------------------------------------\n\r'
    data += 'Authors: Tahir Khan/Tim Schleining\n\r'
    data += '+--------------------------------------------------------------------------+\n\r'
    data += '  Date Run: ' + str(datetime.datetime.now()) + '\n\r'
    data += '+--------------------------------------------------------------------------+\n\r'
    data += '  Input File:   ' + str(file) + '\n\r'
    data += '  Output Path:  ' + str(outputpath) + '\n\r'
    data += '+--------------------------------------------------------------------------+\n\r'
    print(data)
    return data

def Completed():
    data = '| [*] Completed.\n\r'
    data += '+--------------------------------------------------------------------------+\n\r'
    print(data)
    return data


def main(argv):
    #try:
        global verbosity
        report = 'report.html'
        #config = '.\paths.ini'
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
            #else:
             #   shutil.rmtree(path)
        if args.filename:
            filename = args.filename
        if args.config:
            config = args.config
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
        header = Header(path, filename)
        HTMLWriter.htmlwrite('start', '', path, '', '', config)
        #htmlwrite(method, data, ext_filename, ext_name, configfile):
        HTMLWriter.htmlwrite('header', header, path, '', '', config)
        fileype, status, error = IdentifyFile(filename)
        if status:
            print('| [+] File Identified.                                                     |')
        else:
            print('| [-] File Identified.                                                     |')
            Failed(error)
        status, error = hashing.hashFile(filename, path, config, verbosity)
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
        status, error = be.be_call(filename, path, config)
        if status:
            print('| [+] Bulk Extractor Executed.                                             |')
        else:
            print('| [-] Bulk Extractor Executed.                                             |')
            Failed(error)
        status, error = hashing.hashRecursive(path, path, config, verbosity)
        if status:
            print('| [+] Hashing Files.                                                       |')
        else:
            print('| [-] Hashing Files.                                                       |')
            Failed(error)
        status, error = parsebe.parsing(path + 'domain_histogram.txt', path + 'd.txt', config, verbosity)
        if status:
            print('| [+] Parsing Output                                                       |')
        else:
            print('| [-] Parsing Output                                                       |')
            Failed(error)
        #input, output, configfile, verbose
        #status, error = reader.pcapsearch(config, 'C:\\TEMP\\dropbox1.pcap', path)
        status, error = search.grepsearch(path, filename, config, verbosity)

        if status:
            print('| [+] Searching Files                                                      |')
        else:
            print('| [-] Searching Files                                                      |')
            Failed(error)
        Completed()


    #except:
        #sys.exit(0)


main(sys.argv[1:])
