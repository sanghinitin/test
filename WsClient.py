
# -*- coding: utf-8 -*-
"""Simple Web socket client implementation using Tornado framework.
"""
from tornado import escape
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket
import json
import time
import base64
APPLICATION_JSON = 'application/json'
DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 60
class WebSocketClient(object):
    """Base for web socket clients.
    """
    def __init__(self,  connect_timeout=DEFAULT_CONNECT_TIMEOUT,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT):
        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout
    def connect(self, url):
        """Connect to the server.
        :param str url: server URL.
        """
        headers = httputil.HTTPHeaders({'Content-Type': APPLICATION_JSON})
        request = httpclient.HTTPRequest(url=url,
                                         connect_timeout=self.connect_timeout,
                                         request_timeout=self.request_timeout,
                                         headers=headers)
        ws_conn = websocket.WebSocketClientConnection(ioloop.IOLoop.current(),
                                                      request)
        ws_conn.connect_future.add_done_callback(self._connect_callback)
    def send(self, data):
        """Send message to the server
        :param str data: message.
        """
        if not self._ws_connection:
            raise RuntimeError('Web socket connection is closed.')
        if data:
            if data == "pong":
                self._ws_connection.write_message(data)
            else:
                self._ws_connection.write_message(escape.utf8(json.dumps(data)))
    def close(self):
        """Close connection.
        """
        if not self._ws_connection:
            raise RuntimeError('Web socket connection is already closed.')
        self._ws_connection.close()
    def _connect_callback(self, future):
        if future.exception() is None:
            self._ws_connection = future.result()
            self._on_connection_success()
            self._read_messages()
        else:
            self._on_connection_error(future.exception())
    @gen.coroutine
    def _read_messages(self):
        while True:
            msg = yield self._ws_connection.read_message()
            if msg is None:
                self._on_connection_close()
                break
            self._on_message(msg)
    def _on_message(self, msg):
        """This is called when new message is available from the server.
        :param str msg: server message.
        """
        
        pass
    def _on_connection_success(self):
        """This is called on successful connection ot the server.
        """
        pass
    def _on_connection_close(self):
        """This is called when server closed the connection.
        """
        pass
    def _on_connection_error(self, exception):
        """This is called in case if connection to the server could
        not established.
        """
        pass




class TestWebSocketClient(WebSocketClient):
    def _on_message(self, msg):
        print "# -- >  "+msg
        if msg == "ping":
            print "ping aya"
            self.write
        deadline = time.time() + 1
        ioloop.IOLoop().instance()
    def _on_connection_success(self):
        print'Connected!'
        #self.send(str(int(time.time())))
    def _on_connection_close(self):
        print'Connection closed!'
    def _on_connection_error(self, exception):
        print'Connection error: %s', exception
def main():
    #create websocket connection
    client = TestWebSocketClient()
    #wss://tqa.hallwaze.com/hallwaze/chat/ws/1:FE8F198532B758DA02CDFB6C7E78DE1E:79192/
    #client.connect('wss://tqa.hallwaze.com/hallwaze/chat/ws/1:FE8F198532B758DA02CDFB6C7E78DE1E:79192/')
    #5-5f9b4426-33d4-4496-aaa8-f1918a70de53


    client.connect('ws://10.2.1.103:8888/rtm/1/5/5f9b4426-33d4-4496-aaa8-f1918a70de53')

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        client.close()
if __name__ == '__main__':
    main()