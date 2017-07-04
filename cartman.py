#!/bin/sh

import os
import sys
import urllib

import webserver

print ("Test3")

webserver.run(port=8081)

#query = "test3"
#response = urllib.urlopen('http://search.yahoo.com/search?p=%s' % query).read()
#print response