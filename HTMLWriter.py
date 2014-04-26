__author__ = 'khanta'

import HTML
import pyhtml
import datetime
import configparser
import platform


def CreateTable(table_data):
    status = ''
    error = False
    htmlcode = HTML.table(table_data)
    return htmlcode

def htmlwrite(method, data, path, ext_filename, ext_name, configfile):
    system = platform.platform()
    config = configparser.ConfigParser()

    config.read(configfile)
    config.read('C:\\Users\\khanta\\Dropbox\\Git\\MAFA\\paths.ini')
    filename = config.get('Reports', 'reportname')
    filename = path + '\\' + filename
    ext_filename = path + '\\' + ext_filename
    data = data.replace('\n\r', '</br>')
    if method.lower() == 'start':
        with open(filename, 'w+') as output:
            output.write('<html>')
            output.write('<body>')
            output.write('<table>')
            output.write('<h1><center>' + "MAFA Report" + '</center></h12>')
            output.write('<br>')
            output.write('<h3><center>' + "Start Time: " + str(datetime.datetime.now()) + '</center></h3>')
    if method.lower() == 'header':
        with open(filename, 'a') as output:
            output.write('<h2>')
            output.write(data)
            output.write('</h2>')
    if method.lower() == 'table':
        with open(filename, 'a') as output:
            output.write(CreateTable(data))
    if method.lower() == 'data':
        with open(filename, 'a') as output:
            output.write('<br>')
            output.write('<tr><td>' + data + '</td>' + '</tr>')
            output.write('<br>')
    if method.lower() == 'stop':
        with open(filename, 'a') as output:
            output.write('</table>')
            output.write('<h3><center>' + "Stop Time: " + str(datetime.datetime.now()) + '</center></h3>')
            output.write('</body>')
            output.write('</html>')
    if method.lower() == 'external':
        with open(filename, 'a') as output:
            output.write('<br>')
            output.write('<a href=' + ext_filename + '>' + ext_name + '</a>')
            output.write('<br>')
        with open(ext_filename, 'w+') as output:
            output.write('<html>')
            output.write('<body>')
            output.write('<table>')
            output.write('<h1><center>' + ext_name + '</center></h12>')
            output.write('<br>')
            output.write('<h3><center>' + "Start Time: " + str(datetime.datetime.now()) + '</center></h3>')
            output.write('<br>')
            output.write(data)
            output.write('<br>')
            output.write('<h3><center>' + "StopTime: " + str(datetime.datetime.now()) + '</center></h3>')
            output.write('</table>')
            output.write('</body>')
            output.write('</html>')


if __name__ == '__main__':
    filepath = 'c:\\temp\\'
    filename = 'output.htm'
    htmlwrite('start', 'null', filepath + filename, 'null')
    htmlwrite('data', 'hello', filepath + filename, 'null')
    htmlwrite('external', 'Blah Blah', filepath + filename, filepath + 'output1.htm')
    htmlwrite('stop', 'null', filepath + filename, 'null')

