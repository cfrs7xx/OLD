__author__ = 'tschlein'
#Calculates MD5 and SHA-1 hashes for a file or files.

#TODO print to HTML / csv / logfile
#TODO add return with err to main, if determine to be required
#TODO clean up formatting to comply with project semantics

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Description:
#	Calculate MD5 and SHA-1 hashes for a file or files.
#
#	-f | --file <file>          calculate hashes for single file
#	-r | --recursive <path>		recursively hash files in path,
#									top-down
#	-h | --help 				syntax help
#	
# 	
#	Currently written in Python 3.3.2
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os					#path, os.walk() for recursive walking of directories
import fnmatch				#used for file matching
#from subprocess import call	#command line invocations
import sys
import hashlib
import argparse             #http://docs.python.org/3.4/library/argparse.html
#from writer import htmlwrite

def md5(file):

    #define blocksize for reading file
    block = 65536
    #open the file
    f = open(file, 'rb')
    #read in a buffer of size block
    buf = f.read(block)
    #calculate hash
    hash = hashlib.md5()
    #while file has more bytes, update the hash
    while len(buf) > 0:
        hash.update(buf)
        buf = f.read(block)

    return hash


def sha1(file):

    #define blocksize for reading file
    block = 65536
    #open the file
    f = open(file, 'rb')
    #read in a buffer of size block
    buf = f.read(block)
    #calculate hash
    hash =  hashlib.sha1()
    #while file has more bytes, update the hash
    while len(buf) > 0:
        hash.update(buf)
        buf = f.read(block)

    return hash


def main(argv):
    try:
        global debug
        debug = 0

        #Declare list of files.
        files = []

        parser = argparse.ArgumentParser(description="Hash file(s), with recursive hashing as an option.",
                                         add_help=True)
        parser.add_argument('-f', '--file', help='The file to be hashed.', required=False)
        parser.add_argument('-r', '--recursive', help='Recursive hashing.', required=False)
        parser.add_argument('-v', '--verbose', help='The level of debugging.', type=int, required=False)
        parser.add_argument('--version', action='version', version='%(prog)s 0.5')

        args = parser.parse_args()
        if args.file:
            file = args.file
            #add the file to the list
            files.append(file)
        if args.recursive:
            path = args.recursive
            for root, dirnames, filenames in os.walk(path):
            #recursively walk the current path, from the top down (current directory as root)
                for filename in fnmatch.filter(filenames, '*.*'):		#can filter by file type, ex. *.apk
                    #add the files in the present directory to the list
                    files.append(os.path.join(root, filename))
        if args.verbose:
            debug = args.verbose
        if debug >= 1:
            print('Entering Main:')

        #html_file = 'output.htm'
        #htmlwrite('start','null', html_file, 'null')
        #calculate hashes for each file within the file list
        print(files)

        for file in files:
            md5_val = md5(file)
            sha1_val = sha1(file)

            #if file has hash value, print to screen and to html file
            if md5_val:
                #print formatted output string: <filename> TAB <md5 hash> TAB <sha1 hash>
                output = file
                output += '\t'
                output += md5_val.hexdigest()
                output +='\t'
                output += sha1_val.hexdigest()
                print(output)
                #In the future, may return(output) to a driver program, and that program forwards string to HTML_Writing

                #Call HTML_Writing.py from here, sending the string
                #htmlwrite('data',output, html_file, 'null')

        #htmlwrite('stop', 'null', html_file, 'null')

    except IOError:
        sys.exit('Error: File ' + str(file) + ' does not exist.')


#Call main
main(sys.argv[1:])