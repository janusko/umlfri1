from .file import File
from .generator import Generator
from .library import Library
from .template import Template

import os.path
import lxml.etree
from Cheetah.Template import Template as CheetahTemplate

class FileList(object):
    def __init__(self, root):
        self.__fileList = []
        self.__root = root
    
    def parse(self, path):
        dir = os.path.dirname(path)
        rel = lambda f: os.path.abspath(os.path.join(dir, f))
        
        if path.endswith('.py'):
            locals = {}
            globals = {}
            execfile(inputFile, globals, locals)
            for type, params in locals['generate'](self.__root):
                if type == 'file':
                    self.__appendFile(rel(params[0]), params[1])
                elif type == 'generator':
                    self.__appendGenerator(rel(params[0]), params[1])
                elif type == 'library':
                    self.__appendLibrary(rel(params[0]))
                elif type == 'template':
                    self.__appendTemplate(rel(params[0]), params[1])
        else:
            if path.endswith('.xml'):
                data = lxml.etree.parse(path).getroot()
            elif path.endswith('.xml.tmpl'):
                data = lxml.etree.XML(
                    str(CheetahTemplate(file(path).read(), {'root': self.__root}))
                )
            
            for child in data.getchildren():
                if child.tag == 'file':
                    self.__appendFile(rel(child.attrib['path']), child.attrib['output'])
                elif child.tag == 'generator':
                    self.__appendGenerator(rel(child.attrib['path']), child.attrib['output'])
                elif child.tag == 'library':
                    self.__appendLibrary(rel(child.attrib['path']))
                elif child.tag == 'template':
                    self.__appendTemplate(rel(child.attrib['path']), child.attrib['output'])
    
    def create(self, dir):
        for f in self.__fileList:
            f.create(dir)
    
    def __appendFile(self, inputFile, outputFile):
        self.__fileList.append(File(inputFile, outputFile, self.__root))
    
    def __appendGenerator(self, inputFile, outputFile):
        self.__fileList.append(Generator(inputFile, outputFile, self.__root))
    
    def __appendLibrary(self, path):
        self.__fileList.append(Library(path))
    
    def __appendTemplate(self, inputFile, outputFile):
        self.__fileList.append(Template(inputFile, outputFile, self.__root))
