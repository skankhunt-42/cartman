#!/bin/sh

import os
import sys
import urllib

print ("Test3")

query = "test3"
response = urllib.urlopen('http://search.yahoo.com/search?p=%s' % query).read()
print response