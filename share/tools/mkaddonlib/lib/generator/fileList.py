from .file import File
from .generator import Generator
from .template import Template

import sys
import os.path
import lxml.etree
from Cheetah.Template import Template as CheetahTemplate

class FileList(object):
    def __init__(self, builder):
        self.__fileList = []
        self.__builder = builder
    
    def parse(self, path):
        dir = os.path.dirname(path)
        rel = lambda f: os.path.abspath(os.path.join(dir, f))
        
        if os.path.exists(os.path.join(dir, 'lib')):
            sys.path.append(os.path.join(dir, 'lib'))
        
        if path.endswith('.py'):
            locals = {}
            globals = {}
            execfile(inputFile, globals, locals)
            for type, params in locals['generate'](self.__builder.getRootNamespace()):
                if type == 'file':
                    self.__appendFile(rel(params[0]), params[1])
                elif type == 'generator':
                    self.__appendGenerator(rel(params[0]), params[1], params[2])
                elif type == 'template':
                    self.__appendTemplate(rel(params[0]), params[1], params[2])
        else:
            if path.endswith('.xml'):
                data = lxml.etree.parse(path).getroot()
            elif path.endswith('.xml.tmpl'):
                data = lxml.etree.XML(
                    str(CheetahTemplate(file = path, namespaces = {'root': self.__builder.getRootNamespace()}))
                )
            
            for child in data.getchildren():
                if child.tag == 'file':
                    self.__appendFile(rel(child.attrib['path']), child.attrib['output'])
                elif child.tag == 'generator':
                    self.__appendGenerator(rel(child.attrib['path']), child.attrib['output'], child.attrib['root'] or None)
                elif child.tag == 'template':
                    self.__appendTemplate(rel(child.attrib['path']), child.attrib['output'], child.attrib['root'] or None)
    
    def create(self, dir):
        for f in self.__fileList:
            f.create(dir)
    
    def __appendFile(self, inputFile, outputFile):
        self.__fileList.append(File(inputFile, outputFile))
    
    def __appendGenerator(self, inputFile, outputFile, fqn):
        self.__fileList.append(Generator(inputFile, outputFile, self.__builder.getTypeByFQN(fqn)))
    
    def __appendLibrary(self, path):
        self.__fileList.append(Library(path))
    
    def __appendTemplate(self, inputFile, outputFile, fqn):
        self.__fileList.append(Template(inputFile, outputFile, self.__builder.getTypeByFQN(fqn)))
