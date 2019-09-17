from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient

from time import sleep
from random import choice, randint

import sys
import os

DEBUG_OP = os.environ.get('WEBOTS_SOCKET_DEBUG') in ['true', 'True']

CHOICES = ['UP', 'DOWN', 'LEFT', 'RIGHT']


## JUST TO HAVE NAMING IN EACH CLIENT
try:
    CLIENT_NAME = sys.argv[1]
except:
    CLIENT_NAME = 'CLIENT_' + '{}'.format(randint(1000,2000))

class Client(TCPClient):
    """
    This is a simple echo TCP Client
    """
    msg_separator = b'\r\n'

    @gen.coroutine
    def run(self, host, port):
        stream = yield self.connect(host, port)
        while True:
            # data = input(">> ").encode('utf8')
            data = "{}: {}".format(CLIENT_NAME, choice(CHOICES)).encode('utf8')
            data += self.msg_separator
            if not data:
                break
            else:
                yield stream.write(data)
            data = yield stream.read_until(self.msg_separator)
            body = data.rstrip(self.msg_separator)
            sleep(.25)
            if (DEBUG_OP):
                print(body)


if __name__ == '__main__':
    Client().run('localhost', 5567)
    print('Connecting to server socket...')
    IOLoop.instance().start()
    print('Socket has been closed.')