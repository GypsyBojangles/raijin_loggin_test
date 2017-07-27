import pickle
import logging
import logging.handlers
import socketserver
import socket
import struct
import sys
from structlog import wrap_logger
from structlog.processors import JSONRenderer
import time


def add_timestamp(_, __, event_dict):
    event_dict['timestamp'] = int(round(time.time() * 1000))
    event_dict['message'] = event_dict.get('event')
    event_dict.pop('event')
    return event_dict


class LogRecordStreamHandler(socketserver.StreamRequestHandler):

    def handle(self):

        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            self.handleLogRecord(obj['msg'])

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        logger = wrap_logger(
            logging.getLogger(__name__),
            processors=[
                add_timestamp,
                JSONRenderer(sort_keys=True)
            ]
        )
        logger.info(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):

    allow_reuse_address = True

    def __init__(self, host=socket.gethostname(),
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


def main():
    logging.basicConfig(
        stream=sys.stdout,
        level='INFO',
        format='%(message)s,')
    tcpserver = LogRecordSocketReceiver()

    tcpserver.serve_until_stopped()

if __name__ == '__main__':
    main()