import socket, errno

from threading import Thread
try: # Python 2
  from BaseHTTPServer import HTTPServer
  from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError: # Python 3
  from http.server import SimpleHTTPRequestHandler,HTTPServer

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6

def main():
  Thread(target=servev4).start()
  try:
    servev6()
  except OSError as e:
    if not e.errno == errno.EAFNOSUPPORT:
      raise
  
def servev6():
  try:
    server = HTTPServerV6(('::', 81), SimpleHTTPRequestHandler)
    server.serve_forever()
  except socket.error as e:
    if e.errno == errno.EAFNOSUPPORT: # system doesn't support ipv6
      pass
    else:
      raise
  
def servev4():
  server = HTTPServer(('0.0.0.0', 81), SimpleHTTPRequestHandler)
  server.serve_forever()

if __name__ == '__main__':
  main()
