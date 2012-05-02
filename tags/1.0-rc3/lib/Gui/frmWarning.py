from __future__ import with_statement
from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import pango
import lib.Depend
from lib.consts import MAIL, ERROR_LOG_ADDRESS, WEB
from common import CWindow, event
from lib.Distconfig import USERDIR_PATH, ROOT_PATH
from lib.Gui.dialogs import CWarningDialog
import sys, os, time, tarfile, traceback, cStringIO, datetime, urllib, urllib2
import os.path

EXCEPTION_PROJECT_FILE = 'error.frip'


class CfrmWarning(CWindow):
    name = 'frmWarning'
    glade = 'misc.glade'
    
    widgets = ('tviewWarningInfo','tviewWarningSysInfo','btnCancelWarning', 'btnSendWarning',  'btnReportWarning', 'lblWarningMail', 'tviewWarningUsrComment', 'chbtnWarningIncludeProject',)
    
    __modPaths = [os.path.abspath(dir).replace(os.path.sep, "/") for dir in sys.path]
    __modPaths.sort(key=len, reverse=True)

    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        self.lblWarningMail.set_label("<span background='white'><b>"+ MAIL + "</b></span>")
        self.append_project = True

        buff = self.tviewWarningSysInfo.get_buffer()  
        tag_tab = buff.get_tag_table()

        if tag_tab.lookup("bold") is None:
            buff.create_tag("bold", weight=pango.WEIGHT_BOLD, family="monospace")
        if tag_tab.lookup("mono") is None:
            buff.create_tag("mono", family="monospace")
        
        iter = buff.get_iter_at_offset(0)
        buff.insert_with_tags_by_name(iter, "UML .FRI:\t\t", "bold")
        buff.insert_with_tags_by_name(iter, self.application.GetVersion(), "mono")
        try:
            with open(os.path.join(ROOT_PATH, '.svn', 'entries')) as svn:
                result = []
                for idx, line in enumerate(svn):
                    if idx in [3, 4, 10]: 
                        result.append(line[:-1])
                    if idx > 10:
                        break
                result = '%s@%s (%s)' % (result[1], result[2], result[0])
                buff.insert_with_tags_by_name(iter, "\nUML .FRI (svn):\t\t", "bold")
                buff.insert_with_tags_by_name(iter, result, "mono")
        except IOError:
            pass
            
        for name, version in lib.Depend.version():
            buff.insert_with_tags_by_name(iter, "\n%s:\t\t"%name, "bold")
            buff.insert_with_tags_by_name(iter, version, "mono")
    
    @event("chbtnWarningIncludeProject", "toggled", None)
    def OnChbtnIncludeProjectToogled(self, widget, event, data=None):
        if self.append_project == False:
            self.append_project = True
        else :
            self.append_project = False
    
    @event("btnSendWarning", "clicked", None)
    def OnBtnSendClicked(self, widget, event, data=None):
        try:
            output = cStringIO.StringIO()
            tar = tarfile.open(None, "w", output)
            tarinfo = tarfile.TarInfo()
            
            # tarinfo properties
            tarinfo.name = 'error.log'
            tarinfo.type = tarfile.REGTYPE
            tarinfo.mode = 0600
            tarinfo.mtime = time.mktime(datetime.datetime.now().timetuple())
          
            # striongIO for traceback
            buff = self.tviewWarningInfo.get_buffer()
            s, e = buff.get_bounds()
            io_buff =  buff.get_text(s,e)
            iof = cStringIO.StringIO(io_buff)
            iof.seek(0)
            tarinfo.size = len(io_buff)
            tar.addfile(tarinfo, iof)
            iof.close()
           
            # striongIO for sys info
            tarinfo.name = 'sys_info.log'
            buff = self.tviewSysInfo.get_buffer()
            s, e = buff.get_bounds()
            io_buff =  buff.get_text(s,e)
            iof = cStringIO.StringIO(io_buff)
            iof.seek(0)
            tarinfo.size = len(io_buff)
            tar.addfile(tarinfo, iof)
            iof.close()

            # striongIO for comment
            tarinfo.name = 'comment.log'
            buff = self.tviewWarningUsrComment.get_buffer()
            s, e = buff.get_bounds()
            io_buff =  buff.get_text(s,e)
 
            if len(io_buff) > 0:
                iof = cStringIO.StringIO(io_buff)
                iof.seek(0)
                tarinfo.size = len(io_buff)
                tar.addfile(tarinfo, iof)
                iof.close()

            if self.append_project == True:
                if self.application.GetProject() is not None:
                    
                    log_project_path = os.path.join(USERDIR_PATH, EXCEPTION_PROJECT_FILE)
                    self.application.GetProject().SaveProject(log_project_path)
                    tar.add(log_project_path,EXCEPTION_PROJECT_FILE)
                    os.remove(log_project_path)
            

            ### sending....testing ###
            try:
                string_to_send = output.getvalue().encode('base64_codec')
                tar.close() # close tar file
                output.close() # close cStringIO
                
                values = {'upfile' : string_to_send}
                data = urllib.urlencode(values)
                req = urllib2.Request(ERROR_LOG_ADDRESS, data)
                response = urllib2.urlopen(req)

                # if everything goes well
                if response.code == 200:
                    t = _('File successfully send...\n\nThank you for helping improving UML .FRI')
                    self.btnSend.set_sensitive(False)
                
                # not so well, but at least we could get a response :)                
                else:
                    t = _('Uups! Sending was not successfull.\nServer response:\n ') + str(response.code) + ' ' + response.msg
               
            except urllib2.URLError, e :
                t = _('Uups! An error during sending occured:\n') + str(e).replace('<','').replace('>','')
            
            CWarningDialog(None, t).run()
            return

        finally:
            self.form.run()
            self.Hide()


    @event("btnReportWarning", "clicked", None)
    def OnBtnReportClicked(self, widget, event, data=None):
        from webbrowser import open_new
        open_new(WEB)
        self.form.run()
        self.Hide()


    def Show(self):
        self.form.run()
        buff = self.tviewWarningInfo.get_buffer()
        s, e = buff.get_bounds()
        buff.delete(s,e)
        buff = self.tviewWarningUsrComment.get_buffer()
        s, e = buff.get_bounds()
        buff.delete(s,e)
        self.Hide()


    def SetWarningInfo(self, date, warning, category, file, lineno, line):
        file = os.path.abspath(file).replace(os.path.sep, "/")

        for dir in self.__modPaths:
            if file.startswith(dir):
                file = file[len(dir)+1:]
                break
        
        buff = self.tviewWarningInfo.get_buffer()
        tag_tab = buff.get_tag_table()
        iter = buff.get_end_iter()
        
        if tag_tab.lookup("bold") is None:
            buff.create_tag("bold", weight=pango.WEIGHT_BOLD, family="monospace")
        if tag_tab.lookup("mono") is None:
            buff.create_tag("mono", family="monospace")
        buff.insert_with_tags_by_name(iter, 'File ', "bold")
        buff.insert_with_tags_by_name(iter, file,      "mono")
        buff.insert_with_tags_by_name(iter, ' line ',   "bold")
        buff.insert_with_tags_by_name(iter, str(lineno), "mono")
        buff.insert_with_tags_by_name(iter, '\n  ' + (line.strip() or "") + '\n\n', "mono")
        #name and error
        buff.insert_with_tags_by_name(iter, category.__name__  + ': ', "bold")
        buff.insert_with_tags_by_name(iter, str(warning), "mono")
