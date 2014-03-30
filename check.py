__author__ = 'khanta'
__author__ = 'tschlein'

#TODO add Python modules

import sys
from os import path
import platform     #https://docs.python.org/2/library/platform.html
import configparser #https://docs.python.org/2/library/configparser.html
import argparse     #http://docs.python.org/3.4/library/argparse.html


#Check whether the file exists.
def check(file):

    if debug >= 1:
        print('Entering check:')
    if debug >= 2:
        print('\tFile passed in:' + str(file))

    if path.isfile(file):
        if debug >= 2:
            print('\t\t+ ', file)
        return True
    else:
        print('\t\t-', file)
        return False


#Parse the ini file.
def parse(file):
    if debug >= 1:
        print('Entering parse:')
    if debug >= 2:
        print('\tConfig file passed in:' + str(file))

    #Determine system: 'nt' for Windows, 'posix' for *nix, Mac OSX
    system = platform.platform()
    #Determine 32-bit vs. 64-bit architecture
    if platform.architecture()[0] == '64bit':
        architecture = 64
    elif platform.architecture()[0] == '32bit':
        architecture = 32

    #Read the config file for parsing
    config = configparser.ConfigParser()
    config.read(file)

    if 'Windows' in system:
        #Bulk Extractor
        if architecture == 64:
            check(config.get('Windows', '64_bulk'))
        else:
            check(config.get('Windows', '32_bulk'))
        #TShark
        check(config.get('Windows', 'tShark'))

    elif 'Linux' in system:
        #Bulk Extractor
        check(config.get('Linux', '32_bulk'))
        #TShark
        check(config.get('Linux', 'tShark'))


#Parse the command line arguments.
def main(argv):
    try:
        global debug
        debug = 0

        file = './paths.ini'

        parser = argparse.ArgumentParser(description="Check whether required programs and modules exist.",
                                         add_help=True)
        parser.add_argument('-f', '--file', help='The file that contains paths for the required programs and modules.', required=False)
        parser.add_argument('-d', '--debug', help='The level of debugging.', type=int, required=False)
        parser.add_argument('--version', action='version', version='%(prog)s 0.5')

        args = parser.parse_args()
        if args.file:
            file = args.file
            #with codecs.open(file, 'r', 'ascii'):
                #check = True
        if args.debug:
            debug = args.debug
        if debug >= 1:
            print('Entering Main:')

        parse(file)

    except IOError:
        sys.exit('Error: File ' + str(file) + ' does not exist.')


main(sys.argv[1:])