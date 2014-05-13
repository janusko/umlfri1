from VisualObject import CVisualObject
from lib.Math2D import TransformMatrix, Path
from lib.consts import METAMODEL_NAMESPACE
from lib.datatypes import CColor

class CSvg(CVisualObject):
    types = {
        'width': int,
        'height': int,
        'scale': str
    }
    def __init__(self, width, height, scale="1"):
        if scale[-1] == '%':
            self.scale = float(scale[:-1])/100
        else:
            self.scale = float(scale)
        self.width = width
        self.height = height
        self.svg = []
    
    def __parsestyle(self, style):
        ret = {}
        style = style.split(';')
        for line in style:
            name, val = line.split(':')
            name = name.strip()
            val = val.strip()
            if val.lower() == 'none':
                val = None
            ret[name] = val
        return ret
    
    def __parsetransform(self, transform):
        name, attr = transform.split('(')
        attr = [float(i) for i in attr.split(')')[0].split(',')]
        if name == 'translate':
            return TransformMatrix.mk_translation(attr)
        if name == 'matrix':
            return TransformMatrix.mk_matrix(attr)
    
    def __getattrs(self, node):
        ret = {}
        for attr in node.attrib.items():
            ret[attr[0]] = attr[1]
        return ret
    
    def LoadXml(self, element):
        def recursive(parent, transform):
            for node in parent:
                attrs = self.__getattrs(node)
                if 'transform' in attrs:
                    transform = transform*self.__parsetransform(attrs['transform'])
                if node.tag == METAMODEL_NAMESPACE+'path':
                    self.svg.append({'style': self.__parsestyle(attrs.get('style', {})),
                                    'path': transform*Path(attrs.get('d', ''))})
                elif node.tag == METAMODEL_NAMESPACE+'g':
                    recursive(node, transform)
        
        recursive(element, TransformMatrix.mk_scale(self.scale))
    
    def ComputeSize(self, context):
        return self.width * self.scale, self.height * self.scale
    
    def Paint(self, context, canvas):
        trans = TransformMatrix.mk_translation(context.GetPos())
        shadowcolor = context.GetShadowColor()
        
        for path in self.svg:
            if shadowcolor:
                if path['style'].get('fill', None) is None:
                    bgcolor = None
                else:
                    bgcolor = shadowcolor
                color = shadowcolor
            else:
                color = CColor(path['style'].get('stroke', 'black'))
                if 'fill' in path['style'] and path['style']['fill'] is not None:
                    bgcolor = CColor(path['style']['fill'])
                else:
                    bgcolor = None
            canvas.DrawPath(trans*path['path'], color, bgcolor, int(float(path['style'].get('stroke-width', '1').rstrip('px'))+0.5))
