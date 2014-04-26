__author__ = 'tschlein'

#Todo: Add HTML writer or equivalent

import sys
import argparse                 #http://docs.python.org/3.4/library/argparse.html
import string
from bisect import bisect_left
import configparser
import platform

#Source for this function:
# http://stackoverflow.com/questions/2701173/most-efficient-way-for-a-lookup-search-in-a-huge-list-python
def bi_contains(lst, item):
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)


#Sort lines within input file and write to output file
def sort_file(input, output):
    f1 = open(input, 'r')
    f2 = open(output, 'w+')

    lines = f1.readlines()
    lines = sorted(lines)

    for line in lines:
        f2.write(line)

    f2.close()


#Exclude reserved IPv4 addresses
def reserved(line):
    #RFC 1918
    if line.startswith('10.') or line.startswith('192.168.'):
        return False
    elif line.startswith('172.'):
        if int(line[4:6]) >= 12 and int(line[4:6]) <= 31:
            return False

    #RFC's 1700, 6890,
    elif line.startswith('0.') or \
        line.startswith('127.') or \
        line.startswith('169.254') or \
        line.startswith('192.0.2.') or \
        line.startswith('192.88.99.') or \
        line.startswith('192.18.') or \
        line.startswith('192.19.') or \
        line.startswith('192.51') or \
        line.startswith('203.0.113'):
            return False

    elif line.startswith('2'):
        test = line[0:3]
        if test.isdigit():
            if int(test) >= 224 and int(test) <= 255:
                return False

    else:
        return True


def parsing(input, output, configfile, verbose):
    if verbose >= 2:
        print('|[+] Entering parser:')
    system = platform.platform()
    config = configparser.ConfigParser()
    config.read(configfile)
    if 'Windows' in system:
        logfile = 'c:\\temp\\log.txt'
        stop = config.get('Windows', 'stoplist')
    if 'Linux' in system:
        logfile = '/tmp/log_file.txt'
        stop = config.get('Linux', 'stoplist')
    #Open input and output files
    in_file = open(input, 'r+')
    out_file = open(output, 'w+')
    stop_file = open(stop, 'r+')

    #Read lines into memory and then sort (alphabetically)
    lines = in_file.readlines()
    lines = sorted(lines)

    #Stop file must be sorted alphabetically!
    stop_lines = stop_file.readlines()

    for line in lines:
        #Skip commented lines
        if line[0] != '#':
            #Split line with tab as delimiter, then remove first value in tuple (the count)
            line = line.split('\t')[1]

            #Exclude reserved IPv4 addresses
            if reserved(line) == True:
                #Search the exclusion list for domain names
                if not bi_contains(stop_lines, line):
                    out_file.write(line)
                    if verbose >= 2:
                        print('accepted', line)
                else:
                    if verbose >=2:
                        print('denied', line)

    in_file.close()
    out_file.close()
    stop_file.close()

    return True, 'Write to output file complete.'


#
def main():
    try:
        global verbose
        verbose = 0

        parser = argparse.ArgumentParser(description="Parse a given histogram file from Bulk Extractor output.",
                                         add_help=True)
        parser.add_argument('-f', '--file', help='The file to be parsed.', required=True)
        parser.add_argument('-o', '--output', help='The output file.', required=True)
        parser.add_argument('-x', '--exclude', help='The exclusion list.', required=False)
        parser.add_argument('-v', '--verbose', help='The level of debugging.', type=int, required=False)
        parser.add_argument('--version', action='version', version='%(prog)s 0.5')

        args = parser.parse_args()
        if args.verbose:
            verbose = args.verbose
        if args.file:
            file = args.file
        if args.output:
            output = args.output
        if args.exclude:
            exclude = args.exclude
        if verbose >= 1:
            print('Entering Main:')

        parsing(file, output, exclude, verbose)

    except IOError:
        sys.exit('Error: File ' + str(file) + ' does not exist.')


#Call main
if __name__ == '__main__':
    main()