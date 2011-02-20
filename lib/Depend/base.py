import sys

def checkDependencyMet(condition, message, optional = False):
    if not condition:
        if optional:
            print message
        else:
            raise AssertionError(message)
