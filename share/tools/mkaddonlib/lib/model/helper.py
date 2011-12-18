import re

def computeInterfaceApiName(name):
    return ('I' + name).upperCamelCase

def computeMethodApiName(singular):
    return singular.upperCamelCase

def computeMethodParameterApiName(singular):
    return singular.lowerCamelCase

def computePropertyIndexApiName(singular):
    return singular.lowerCamelCase

def computePropertyGetterApiName(singular, plural):
    return ('get' + singular).upperCamelCase

def computePropertySetterApiName(singular, plural):
    return ('set' + singular).upperCamelCase

def computePropertyIteratorApiName(singular, plural):
    return ('get' + plural).upperCamelCase


def computeEventApiName(identifier):
    return identifier.lowerDashSeparated
