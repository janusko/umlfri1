def Indent(elem, level=0):
    """
    The indent function is a variant of the one in Fredrik Lundh's effbotlib.
    This function make XML Tree more human friendly.
    
    @param  elem: XML element to parse
    @type   elem: L{Element<xml.etree.ElementTree.Element>}
    
    @param  level: level of element
    @type   level: integer
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            Indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def ToBool(val):
    """
    Convert any value to boolean
    
    @param val: value to convert
    @type  val: string
    
    @return: boolean value of given parameter
    @rtype:  boolean
    """
    if type(val) in (str, unicode):
        return val.lower() in ('1', 'yes', 'true')
    else:
        return val == True

def XMLEncode(val):
    """
    Encode given parameter for usage in XML files
    
    @param val: normal string
    @type  val: string
    
    @return: xml encoded value
    @rtype:  string
    """
    ret = repr(val)
    if isinstance(val, str):
        ret = ret[1:-1]
    elif isinstance(val, unicode):
        ret = ret[2:-1]
    return ret.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('<', '&gt;').replace('"', '&quot;').encode('utf8')

def ParseScale(val):
    """
    Parses scale from string into float.

    @param val: scale as defined in metamodel schema (float in range 0.0-1.0 or in percentage form)
    @type  val: str

    @return: scale as floating-point number in range 0.0-1.0
    @rtype : float
    """
    if val[-1] == '%':
        return float(val[:-1])/100
    else:
        return float(val)
