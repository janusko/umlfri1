import thread, base64, array
from CommandParser import CCommandParser
from SynchLineBuffer import CSynchLineBuffer
from ComSpec import *
from lib.consts import PLUGIN_DISPLAY_COMMUNICATION
from lib.Addons.Plugin.Communication.Medium import MediumError, MediumTimeout

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
                        fline = '%s/%s %i %s' % (IDENTIFIER, VERSION, command, type)
                    else:
                        fline = '%s/%s %i' % (IDENTIFIER, VERSION, command, )
                else:
                    fline = '%s %s %s/%s' % (command, type, IDENTIFIER, VERSION)
                
                pline = '\n'.join( (str(key) + ': ' + str(value)) for key, value in params.iteritems())
                
                if data:
                    data = '%s\n%s\n\n%s\n\n' % (fline, pline, data)
                else:
                    data = '%s\n%s\n\n\n' % (fline, pline)
                    
                if PLUGIN_DISPLAY_COMMUNICATION and self.client:
                    for line in data.splitlines():
                        print `line+'\n'`
                
                self.sock.Send(data)
                result = True
            
            except MediumTimeout:
                pass
            
            except MediumError:
                self.state = False
            
            finally:
                self.lock.release()
        return result
        
    def Close(self):
        '''
        Close socket
        '''
        self.state = False
        self.sock.Close()
    
    def Opened(self):
        '''
        @return: True if socket is opened
        '''
        if not self.state:
            return False
        else:
            self.state = self.sock.IsOpened()
            return self.state
