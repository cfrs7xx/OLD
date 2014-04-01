__author__ = 'tschlein'
#Checks for existence of dependencies (executable files, Python modules).
#Returns True if all dependencies are present; otherwise, returns False and prints missing files.

#TODO add Python modules

import sys
from os import path
import platform     #https://docs.python.org/2/library/platform.html
import configparser #https://docs.python.org/2/library/configparser.html
import argparse     #http://docs.python.org/3.4/library/argparse.html


#Parse the ini file to check whether dependencies are present.
def parse(file):
    if debug >= 1:
        print('Entering parse:')
    if debug >= 2:
        print('\tConfig file passed in:' + str(file))

    #Declare list of missing executables and/or modules.
    missing = []

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
        for key in config['Windows']:
            value = config.get('Windows', key)
            if path.isfile(value):
                if debug >= 2:
                    print('\t| [+]  ', value, '|')
            else:
                print('\t| [-]  ', value, '|')
                missing.append(value)

    elif 'Linux' in system:
        for key in config['Linux']:
            value = config.get('Linux', key)
            if path.isfile(value):
                if debug >= 2:
                    print('\t| [+]  ', value, '|')
            else:
                print('\t| [-]  ', value, '|')
                missing.append(value)

    #Return True if all dependencies are present; otherwise, return False.
    if (len(missing)):
        return False
    else:
        return True

#Parse the command line arguments.
def main(argv):
    try:
        global debug
        debug = 0

        file = './paths.ini'

        parser = argparse.ArgumentParser(description="Check whether required programs and modules exist.",
                                         add_help=True)
        parser.add_argument('-f', '--file', help='The file that contains paths for the required programs and modules.', required=False)
        parser.add_argument('-v', '--verbose', help='The level of debugging.', type=int, required=False)
        parser.add_argument('--version', action='version', version='%(prog)s 0.5')

        args = parser.parse_args()
        if args.file:
            file = args.file
        if args.verbose:
            debug = args.verbose
        if debug >= 1:
            print('Entering Main:')

        value = parse(file)
        return(value)

    except IOError:
        sys.exit('Error: File ' + str(file) + ' does not exist.')


main(sys.argv[1:])