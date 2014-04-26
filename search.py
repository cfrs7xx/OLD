__author__ = 'khanta'

from subprocess import call
import subprocess
import HTMLWriter
import configparser
import platform
#import searchbin

def grepsearch(path, filename, configfile, verbosity): #path, filename, config, verbosity
    status = True
    error = ''
    logfile = ''
    return_code = 0
    queries = []

    system = platform.platform()
    config = configparser.ConfigParser()
    config.read(configfile)
    data = ''

    if 'Windows' in system:
        logfile = 'c:\\temp\\log.txt'
        grep = config.get('Windows', 'grep')
    if 'Linux' in system:
        logfile = '/tmp/log_file.txt'
        grep = config.get('Linux', 'grep')
    for key in config['SearchesRegular']:
        value = config.get('SearchesRegular', key)
        query = (str.strip(value, "\""))
        proc = subprocess.Popen([grep, '--byte-offset', '--only-matching', '--text', query, filename], stdout=subprocess.PIPE, stderr=None)
        #proc = subprocess.Popen([grep,'-h', '-b', '-z', '-a', '-i', '-r', query, filename], stdout=subprocess.PIPE, stderr=None)
        out = proc.communicate()[0]

        if out != b'':
            #print ('Results for ' + str(key) + ': ' + str(out.decode("utf-8")))
            #(method, data, filename, ext_filename, ext_name):
            data += str(out)
        HTMLWriter.htmlwrite('external', data, path, key + '-searches.html', key, configfile)
        data = ''
        #print (data)
    #data1 =  data.split('\x00')
    #print (data)

    #method, data, path, ext_filename, ext_name, configfile
        #sys.exit()




    if return_code == 0:
        status = True
    else:
        status = False

    return status, error






