__author__ = 'khanta'
__author__ = 'tschlein'

from subprocess import call
import os
import configparser
import platform

def be_call(filename, path, configfile, verbose):
    status = True
    error = ''
    logfile = ''
    if verbose >= 2:
        print(' [+] Entering be_call: ')
    config = configparser.ConfigParser()
    config.read(configfile)
    system = platform.platform()

    if 'Windows' in system:
        logfile = 'c:\\temp\\log.txt'
        bulkex = config.get('Windows', '32_Bulk')
    elif 'Linux' in system:
        for key in config['Linux']:
            bulkex = config.get('Linux', 'bulk')
        logfile = '/tmp/log_file.txt'
    if verbose >= 2:
        print('\t[+] About to open logfile: ')
    #try:
    #with open('/tmp/log_file.txt', 'a') as log:
    with open(logfile, 'a+') as log:
        return_code = call([bulkex, '-o', path, '-q', '-1', filename], stdout=log, stderr=None)
    if return_code == 0:
        status = True
    else:
        status = False
    return status, error


