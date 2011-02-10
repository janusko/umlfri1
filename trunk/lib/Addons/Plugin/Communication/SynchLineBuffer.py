from lib.Addons.Plugin.Communication.Medium import MediumError, MediumTimeout

class CSynchLineBuffer(object):
    '''
    object reads from socket. Reading is blocking and executes in the callers thread
    '''
    
    def __init__(self, sock):
        '''
        @param sock: connected socket object
        '''
        self.sock = sock
        self.buf = []
        self.state = True
        self.last = ''
    
    def _reload(self):
        '''
        reads from socket some data and splits them to lines.
        puts lines to buffer.
        waits if there is no data in socket to be read.
        '''
        if self.state:
            try:
                data = self.sock.Recv(0x10000)
            except MediumTimeout:
                return
            except MediumError:
                self.state = None
                self.sock.Close()
                return
            if data == '':
                self.state = None
                self.sock.Close()
                return
            data = ''.join((self.last, data))
            lines = data.splitlines(True)
            if not data.endswith(('\r','\n')):
                self.last = lines.pop()
            else:
                self.last = ''
            self.buf += lines
        else:
            return
    
    def read(self):
        '''
        @return: one line of text read from socket
        '''
        while (not self.buf) and self.state:
            self._reload()
        if self.buf:
            return self.buf.pop(0)
        else:
            return None
