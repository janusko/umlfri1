import thread, base64, array, socket
from CommandParser import CCommandParser
from SynchLineBuffer import CSynchLineBuffer
from ComSpec import *


class CSocketWrapper(object):
    
    def __init__(self, sock, proxy, addr, client):
        '''
        @param sock: connected socket object
        @param proxy: object with proxy interface - must have Command, Stopped and Error method
        @param addr: identifier of socket wrapper - used as parameter for proxy interface
        @param client: true if called from worker application, false in manager application
        '''
        self.lock = thread.allocate()
        self.sock = sock
        self.state = True
        self.client = client
        self.parser = CCommandParser(CSynchLineBuffer(sock), proxy, client, addr)
    
    def Send(self, command, type = '', params = {}, data = '', encode = True):
        '''
        send message over socket
        
        
        @param command: command name or response code
        @param type: command first parameter or response description
        @param params: dictionary of parameters
        @param data: string or array to be send as data of message
        @param encode: if true, base64 encoding will be used for data
        '''
        
        result = False
        if self.Opened():
            try:
                self.lock.acquire()
                if isinstance(data, unicode):
                    data = data.encode('utf-8')
                elif isinstance(data, array.array):
                    data = data.tostring()
                    
                if isinstance(data, str):
                    if encode:
                        data = base64.encodestring(data)
                else:
                    raise ValueError('cannot send data')
                    
                if self.client:
                    if type:
                        fline = '%s/1.0 %i %s' % (IDENTIFIER, command, type)
                    else:
                        fline = '%s/1.0 %i' % (IDENTIFIER, command, )
                else:
                    fline = '%s %s %s/1.0' % (command, type, IDENTIFIER)
                
                pline = '\n'.join( (str(key) + ': ' + str(value)) for key, value in params.iteritems())
                
                if data:
                    data = '%s\n%s\n\n%s\n\n' % (fline, pline, data)
                else:
                    data = '%s\n%s\n\n\n' % (fline, pline)
                    
                self.sock.sendall(data)
                result = True
            
            except socket.timeout:
                pass
            
            except socket.error:
                self.state = False
            
            finally:
                self.lock.release()
        return result
        
    def Close(self):
        '''
        Close socket
        '''
        self.state = false
        self.socket.close()
    
    def Opened(self):
        '''
        @return: True if socket is opened
        '''
        if not self.state:
            return False
        else:
            self.state = not isinstance(self.sock._sock, socket._closedsocket)
            return self.state
