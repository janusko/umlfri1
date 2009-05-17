from plugin import CCriticalPathFinder
import time

def main(interface):
    CCriticalPathFinder(interface)
    interface.WaitTillClosed()
