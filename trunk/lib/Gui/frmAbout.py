# -*- coding: utf-8 -*-

from lib.Depend.gtk2 import pango
import lib.Depend

from common import CWindow, event
from lib.Distconfig import IMAGES_PATH, DOCS_PATH
from lib.consts import WEB
import os.path

import re
import webbrowser

class CfrmAbout(CWindow):
    name = 'frmAbout'
    glade = 'help.glade'
    
    widgets = ('tviewCredits','tviewAboutSysInfo', 'lblAboutUmlfri', 'lbtnProjectWeb', 'imgLogo')
    
    reProgrammedFor = re.compile('^Programmed for:$')
    reProgrammedBy = re.compile('^Programmed by:$')
    reSupervisedBy = re.compile('^Supervised by:$')
    reAcademicYear = re.compile('^  Academic year ([0-9]{4}):$')
    
    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        
        self.imgLogo.set_from_file(os.path.join(IMAGES_PATH, 'app_logo.png'))
        
        buff = self.tviewAboutSysInfo.get_buffer()  
        tag_tab = buff.get_tag_table()

        if tag_tab.lookup("bold") is None:
            buff.create_tag("bold", weight=pango.WEIGHT_BOLD, family="monospace")
        if tag_tab.lookup("mono") is None:
            buff.create_tag("mono", family="monospace")
        
        iter = buff.get_iter_at_offset(0)
        begin = ''
        
        l = 0
        for name, version in lib.Depend.version():
            l = max(l, len(name.decode('utf8')))
        
        for name, version in lib.Depend.version():
            buff.insert_with_tags_by_name(iter, begin+((u"%%-%ds  : "%l)%name.decode('utf8')).encode('utf8'), "bold")
            buff.insert_with_tags_by_name(iter, version, "mono")
            begin = '\n'
        
        self.showport = False
        self.lengthname = l
        self.textiter = iter
        self.buff = buff
    
    def Show(self):
        # clear the buffer
        buff = self.tviewCredits.get_buffer()
        s, e = buff.get_bounds()
        buff.delete(s,e)
        # set the about info
        text = '<span size="xx-large">UML .FRI</span>\n<b>' + _('Version') + ' ' + self.application.GetVersionString() + '</b>\n\n' + _('Free python-based CASE tool.')
        self.lblAboutUmlfri.set_use_markup(True)
        self.lblAboutUmlfri.set_label(text)
        # set credits
        self.__SetCredits()
        # set web address 
        self.lbtnProjectWeb.set_uri(WEB)
        self.lbtnProjectWeb.set_label(WEB)
        
        if not self.showport:
            port = self.application.GetPluginPort()
            if port:
                self.buff.insert_with_tags_by_name(self.textiter, ((u"\n%%-%ds  : "%self.lengthname)%u"Plugin port").encode('utf8'), 'bold')
                self.buff.insert_with_tags_by_name(self.textiter, str(port), 'mono')
            self.showport = True
        
        self.form.run()
        self.Hide()
        
    @event("lbtnProjectWeb", "clicked")
    def OnLbtnProjectWebClicked(self, widget):
        webbrowser.open_new_tab(WEB)
        self.form.run()
        self.Hide()
    
    def __Replace(self, line, re, txt):
        match = re.match(line)
        if match:
            return txt%match.groups(), True
        else:
            return line, False

    def __SetCredits(self):
        buff = self.tviewCredits.get_buffer()
        tag_tab = buff.get_tag_table()
        iter = buff.get_end_iter()

        if tag_tab.lookup("bold") is None:
            buff.create_tag("bold", weight=pango.WEIGHT_BOLD)

        lines = [line.rstrip() for line in file(os.path.join(DOCS_PATH, 'ABOUT')) if not line.strip().startswith('-')]
 
        for line in lines:
            i = self.reProgrammedFor.match(line) is not None
            replaced = False
            for re, txt in [
                                (self.reAcademicYear, '  '+_('Academic year %s:')),
                                (self.reProgrammedBy, _('Programmed by:')),
                                (self.reProgrammedFor, _('Programmed for:')),
                                (self.reSupervisedBy, _('Supervised by:')),
                            ]:
                if not replaced:
                    line, replaced = self.__Replace(line, re, txt)
            if replaced:
                ignore = i
                buff.insert_with_tags_by_name(iter, line+'\n', "bold")
            elif not ignore:
                buff.insert(iter, line+'\n')
            if i:
                buff.insert(iter, '    '+_(u'University of Žilina')+'\n')
                buff.insert(iter, '    '+_('Fakulty of Management Science and Informatics')+'\n')
                buff.insert(iter, '\n')
