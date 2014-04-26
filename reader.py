__author__ = 'khanta'

from subprocess import call
import subprocess
import HTMLWriter
import configparser
import platform
from collections import Counter

def pcapsearch(configfile, filename, path):
    status = True
    error = ''
    logfile = ''
    return_code = 0
    data1 = []
    debug = 0
    system = platform.platform()
    config = configparser.ConfigParser()
    config.read(configfile)
    data = ''

    if 'Windows' in system:
        logfile = 'c:\\temp\\log.txt'
        tshark = config.get('Windows', 'tshark')
    if 'Linux' in system:
        logfile = '/tmp/log_file.txt'
        tshark = config.get('Linux', 'tshark')
    for key in config['SearchesRegular']:
        value = config.get('SearchesRegular', key)
        query =  (str.strip(value, "\""))
        proc = subprocess.Popen([tshark, '-r', filename, '-Y', 'ssl.handshake.certificate', '-T', 'fields', '-e', 'x509sat.uTF8String'], stdout=subprocess.PIPE, stderr=None)
        out = proc.communicate()[0].decode("utf-8")
        data1 = out.split('\n')
        proc = subprocess.Popen([tshark, '-r', filename, '-Y', 'ssl.handshake.certificate', '-T', 'fields', '-e', 'x509sat.uTF8String'], stdout=subprocess.PIPE, stderr=None)
        out = proc.communicate()[0].decode("utf-8")
        print (Counter(data1))

    return status, error