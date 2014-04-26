from .Implementation.PipeChannel import CPipeChannel

from multiprocessing.forking import duplicate

import os
import os.path
import subprocess
import signal

try:
    from exceptions import WindowsError
except ImportError:
    class WindowsError(Exception):
        """
        Never occuring exception. WindowsError replacement for non-windows system.
        """

STARTERS = {}

class CBaseProgramStarter:
    program = ()
    environment = {}
    
    def __init__(self, plugin):
        self.__plugin = plugin
    
    def Start(self):
        channel = CPipeChannel()
        
        path = self.__plugin.GetPath()
        uri = self.__plugin.GetUri()
        
        env = os.environ.copy()
        env['UMLFRI_URI'] = str(uri)
        env['UMLFRI_PATH'] = str(path)
        
        for name, value in self.environment.iteritems():
            env['UMLFRI_' + name] = value
        
        program = [part.format(path = path) for part in self.program]
        
        if os.name == 'nt':
            import msvcrt
            ppin = duplicate(msvcrt.get_osfhandle(channel.GetReaderFD()), inheritable=True)
            ppout = duplicate(msvcrt.get_osfhandle(channel.GetWriterFD()), inheritable=True)
            env['UMLFRI_PIN'] = str(ppin)
            env['UMLFRI_POUT'] = str(ppout)
            ppin = msvcrt.open_osfhandle(ppin, os.O_RDONLY)
            ppout = msvcrt.open_osfhandle(ppout, os.O_APPEND)
            self.__process = subprocess.Popen(program, close_fds = False, env = env)
            channel.CloseOthers()
            os.close(ppin)
            os.close(ppout)
            
        else:
            env['UMLFRI_PIN'] = str(channel.GetReaderFD())
            env['UMLFRI_POUT'] = str(channel.GetWriterFD())
            pid = os.fork()
            if pid:
                #parent
                self.__pid = pid
                channel.CloseOthers()
            else:
                #child
                channel.Close()
                os.execve(program[0], program, env)
        
        return channel
    
    def Terminate(self):
        if os.name == 'nt':
            try:
                self.__process.terminate()
            except WindowsError:
                if self.__process.poll() is None:
                    raise

        else:
            os.kill(self.__pid, signal.SIGTERM)
        
    def Kill(self):
        if os.name == 'nt':
            try:
                self.__process.kill()
            except WindowsError:
                if self.__process.poll() is None:
                    raise
        else:
            os.kill(self.__pid, signal.SIGKILL)
    
    def IsAlive(self):
        if os.name == 'nt':
            return self.__process.poll() is None
        else:
            try:
                return (0, 0) == os.waitpid(self.__pid, os.WNOHANG)
            except:
                return False
    
    def GetPid(self):
        if os.name == 'nt':
            return self.__process.pid
        else:
            return self.__pid
