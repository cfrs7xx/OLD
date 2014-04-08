__author__ = 'khanta'


import HTML
import pyhtml

def CreateTable(table_data):
    status = ''
    error = False
    htmlcode = HTML.table(table_data)

    return status, error, htmlcode
