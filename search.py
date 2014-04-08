__author__ = 'khanta'

from subprocess import call
import subprocess
import sys
import configparser


def grepsearch(configfile, filename, path):
    status = True
    error = ''
    logfile = ''
    return_code = 0
    queries = []
    debug = 0

    config = configparser.ConfigParser()
    config.read(configfile)

    grep = 'c:\\tools\grep.exe'
    for key in config['SearchesRegular']:
        value = config.get('SearchesRegular', key)
        query =  (str.strip(value, "\""))
        proc = subprocess.Popen([grep, '-b', '-w', '-z', '-a', '-i', '-r', query, path], stdout=subprocess.PIPE, stderr=None)
        out = proc.communicate()[0]

        if out != b'':
            #print ('Results for ' + str(key) + ': ' + str(out.decode("utf-8")))
            print ('Results for ' + str(key) + ': ' + str(out))
        #sys.exit()




    if return_code == 0:
        status = True
    else:
        status = False

    return status, error
