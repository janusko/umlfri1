from plugin import CCriticalPathFinder

def main(interface):
    CCriticalPathFinder(interface)
    interface.WaitTillClosed()
