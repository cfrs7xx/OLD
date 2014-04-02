__author__ = 'tschlein'

#Todo: Add exclusion list

import sys
import argparse                 #http://docs.python.org/3.4/library/argparse.html
from bisect import bisect_left

#Source for this function:
# http://stackoverflow.com/questions/2701173/most-efficient-way-for-a-lookup-search-in-a-huge-list-python
def bi_contains(lst, item):
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)


def parsing(input, output, stop, verbose):
    if verbose >= 1:
        print('|[+] Entering parser:')

    #Open input and output files
    in_file = open(input, 'r+')
    out_file = open(output, 'w+')
    stop_file = open(stop, 'r+')

    #Read lines into memory and then sort (alphabetically)
    lines = in_file.readlines()
    lines = sorted(lines)

    stop_lines = stop_file.readlines()

    for line in lines:
        #Skip commented lines
        if line[0] != '#':
            #Split line with tab as delimiter, then remove first value in tuple (the count)
            line = line.split('\t')[1]

            #if not bi_contains(stop_lines, line):
            #    out_file.write(line)
            #    if verbose >= 2:
            #        print(line)
            #else:
            #    print('hi', line)

    in_file.close()
    out_file.close()

    return True


def main(argv):
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
main(sys.argv[1:])