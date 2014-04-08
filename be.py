__author__ = 'khanta'
__author__ = 'tschlein'

from subprocess import call
import os

def be_call(filename, path, oper):
    status = True
    error = ''
    logfile = ''

    if oper == 'Windows':
        logfile = 'c:\\temp\\log.txt'
        bulkex = 'c:\\Program Files (x86)\\Bulk Extractor 1.4.1\\32-bit\\bulk_extractor.exe'
    if oper == 'Linux':
        logfile = '/tmp/log_file.txt'
        bulkex = 'bulk_extractor.exe'

    #try:
    #with open('/tmp/log_file.txt', 'a') as log:
    with open(logfile, 'a+') as log:
        return_code = call([bulkex, '-o', path,'-q', '-1', filename], stdout=log, stderr=None)
    if return_code == 0:
        status = True
    else:
        status = False

    return status, error


