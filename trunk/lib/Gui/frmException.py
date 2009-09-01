from __future__ import with_statement
from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import pango
import lib.Depend
import lib.consts
from common import CWindow
from lib.Distconfig import USERDIR_PATH, ROOT_PATH
from lib.Gui.dialogs import CWarningDialog
import sys, os, time, tarfile, traceback, cStringIO, datetime, urllib, urllib2
import os.path

EXCEPTION_PROJECT_FILE = 'error.frip'


class CfrmException(CWindow):
    name = 'frmException'
    glade = 'misc.glade'
    
    widgets = ('tviewErrorLog','tviewSysInfo','btnCancel', 'btnSend',  'btnReport', 'ntbkException', 'lblMail', 'tviewUsrComment', 'chbtnIncludeProject',)
    
    __modPaths = [os.path.abspath(dir).replace(os.path.sep, "/") for dir in sys.path]
    __modPaths.sort(key=len, reverse=True)

    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        # using connect, @event could not be used cause this dialog is used in lib.Gui.event
        self.btnReport.connect("clicked", self.OnBtnReportClicked, None)
        self.btnSend.connect("clicked", self.OnBtnSendClicked, None)
        self.chbtnIncludeProject.connect("toggled", self.OnChbtnIncludeProjectToogled, None)
        self.lblMail.set_label("<span background='white'><b>"+ lib.consts.MAIL + "</b></span>")
        self.append_project = True

        buff = self.tviewSysInfo.get_buffer()  
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
    
    def OnChbtnIncludeProjectToogled(self, widget, event, data=None):
        if self.append_project == False:
            self.append_project = True
        else :
            self.append_project = False
 
       
    def OnBtnSendClicked(self, widget, event, data=None):
        try:
            log_tar_path = os.path.join(USERDIR_PATH, str(time.time()) + '.tar')  # path to tar file
            tar = tarfile.open(log_tar_path, "w")
            tarinfo = tarfile.TarInfo()
            
            # tarinfo properties
            tarinfo.name = 'error.log'
            tarinfo.type = tarfile.REGTYPE
            tarinfo.mode = 0600
            tarinfo.mtime = time.mktime(datetime.datetime.now().timetuple())
          
            # striongIO for traceback
            buff = self.tviewErrorLog.get_buffer()
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
            buff = self.tviewUsrComment.get_buffer()
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
            
            tar.close() # closing the tar file, now we have all we need for sending

            ### sending....testing ###
            try:
                file_to_send = open(log_tar_path, 'r')            
                string_to_send = file_to_send.read().encode('base64_codec')
                file_to_send.close()
                
                values = {'upfile' : string_to_send}
                data = urllib.urlencode(values)
                req = urllib2.Request(lib.consts.ERROR_LOG_ADDRESS, data)
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
            
            os.remove(log_tar_path)     # remove the tar-ed log file
            CWarningDialog(None, t).run()
            return

        finally:
            self.form.run()
            self.Hide()


    def OnBtnReportClicked(self, widget, event, data=None):
        from webbrowser import open_new
        open_new(lib.consts.WEB)
        self.form.run()
        self.Hide()


    def Show(self):
        self.form.run()
        buff = self.tviewErrorLog.get_buffer()
        s, e = buff.get_bounds()
        buff.delete(s,e)
        buff = self.tviewUsrComment.get_buffer()
        s, e = buff.get_bounds()
        buff.delete(s,e)
        self.Hide()


    def SetErrorLog(self, exccls, excobj, tb):
        buff = self.tviewErrorLog.get_buffer()
        tag_tab = buff.get_tag_table()
        iter = buff.get_end_iter()
        
        if tag_tab.lookup("bold") is None:
            buff.create_tag("bold", weight=pango.WEIGHT_BOLD, family="monospace")
        if tag_tab.lookup("mono") is None:
            buff.create_tag("mono", family="monospace")

        for filename, line_num, fun_name, text in traceback.extract_tb(tb)[1:]:
            filename = os.path.abspath(filename).replace(os.path.sep, "/")
            for dir in self.__modPaths:
                if filename.startswith(dir):
                    filename = filename[len(dir)+1:]
                    break
            buff.insert_with_tags_by_name(iter, 'File ', "bold")
            buff.insert_with_tags_by_name(iter, filename,      "mono")
            buff.insert_with_tags_by_name(iter, ' line ',   "bold")
            buff.insert_with_tags_by_name(iter, str(line_num), "mono")
            buff.insert_with_tags_by_name(iter, ' in ',     "bold")
            buff.insert_with_tags_by_name(iter, (fun_name or "") + '\n  ' + (text or "") + '\n\n', "mono")
        #name and error
        buff.insert_with_tags_by_name(iter, exccls.__name__  + ': ', "bold")
        buff.insert_with_tags_by_name(iter, str(excobj), "mono")
