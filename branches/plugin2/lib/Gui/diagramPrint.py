# -*- coding: utf-8 -*-
from lib.Depend.gtk2 import gtk
from lib.Exceptions.UserException import PrintError
from lib.Drawing.Canvas import CPrintCanvas
from lib.Gui.dialogs import CWarningDialog
from lib.Depend.gtk2 import gobject
import math

#gtk.UNIT_PIXEL
#gtk.UNIT_POINTS
#gtk.UNIT_INCH
#gtk.UNIT_MM

class CDiagramPrint(gobject.GObject):

    def __init__(self):
        gobject.GObject.__init__(self)
        self.settings = gtk.PrintSettings()
        self.page_setup = gtk.PageSetup()
        self.print_operation = None
        # matrix with (x,y) coordinates that refer to the start
        # position in self.diagram that will be printed
        # on current page, e.g. if it is (0,0), then area
        # from 0,0 to 0 + self.pageWidth, 0 + self.pageHeight
        # will be printed on current page -- funky :)
        self.print_matrix = []
        self.cur_matrix_pos = 0
                    

    def printPropertiesSetup(self, parent = None):
        self.page_setup = gtk.print_run_page_setup_dialog(parent, self.page_setup, self.settings)


    def printStart(self, diagram, use_margins = False):
        # if true, we will be printing on margins too
        self.use_margins = use_margins
        self.diagram = diagram
        self.print_operation = gtk.PrintOperation()
        self.print_operation.set_unit(gtk.UNIT_POINTS)
        # do we really need this ? no...
        # self.print_operation.set_job_name(_("UML .FRI diagram print"))
        
        if self.settings is not None:
            self.print_operation.set_print_settings(self.settings)

        if self.page_setup is not None:
           self.print_operation.set_default_page_setup(self.page_setup)
        
        self.print_operation.connect("preview", self.preview)
        self.print_operation.connect("begin_print", self.beginPrint)
        self.print_operation.connect("draw_page", self.drawPage)

        print_res = self.print_operation.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)
        
        if print_res == gtk.PRINT_OPERATION_RESULT_APPLY:
            self.settings = self.print_operation.get_print_settings()
        elif print_res ==  gtk.PRINT_OPERATION_RESULT_ERROR:
            raise PrintError(_("An error during printing has occured."))
        elif print_res ==  gtk.PRINT_OPERATION_RESULT_CANCEL:      
            pass
       
        
    def preview (self, operation, preview, context, parent):
        # nasty method... what to do if we do _not_ have evince ??
        pass 


    def beginPrint(self,operation, context):
        canvas = CPrintCanvas(context.get_cairo_context())
        # getting diagram size square, perhaps it would be better
        # to implement a new method to prevent blank pages,
        # because diagram.GetExpSquare gets one biiig square
        diagram_width, diagram_height = self.diagram.GetExpSquare()
        # re-set matrix
        self.cur_matrix_pos = 0
        self.print_matrix = []
        
        if self.use_margins:
            self.page_width = self.page_setup.get_page_width(gtk.UNIT_POINTS) +  \
                              self.page_setup.get_left_margin(gtk.UNIT_POINTS) + \
                              self.page_setup.get_right_margin(gtk.UNIT_POINTS)
            
            self.page_height = self.page_setup.get_page_height(gtk.UNIT_POINTS) +   \
                               self.page_setup.get_bottom_margin(gtk.UNIT_POINTS) + \
                               self.page_setup.get_top_margin(gtk.UNIT_POINTS)
        else:
            self.page_width = self.page_setup.get_page_width(gtk.UNIT_POINTS)
            self.page_height = self.page_setup.get_page_height(gtk.UNIT_POINTS)
       
        horizontal_page_count = int(math.ceil(diagram_width/self.page_width))
        vertical_page_count = int(math.ceil(diagram_height/self.page_height))
        
        for i in range(vertical_page_count):
            for j in range(horizontal_page_count):
                self.print_matrix.append((j*self.page_width, i*self.page_height))
                 
        operation.set_n_pages(horizontal_page_count * vertical_page_count)


    def drawPage(self, operation, context, page_nr):
        cr = context.get_cairo_context()
        # crazy math and the funky matrix
        x = int(math.floor(self.print_matrix[self.cur_matrix_pos][0]))
        y = int(math.floor(self.print_matrix[self.cur_matrix_pos][1]))
        area_to_print = ((x, y),(x + int(math.floor(self.page_width)), y + int(math.floor(self.page_height))))
        canvas = CPrintCanvas(cr)
        self.diagram.SetViewPort(area_to_print)
        self.diagram.Paint(canvas)
        # we need to reset cur_matrix_pos if it wants to
        # grow bigger then print_matrix size -- this happens
        # when user chooses multiple copies: gtk.PrintSettings.get_n_copies
        if len(self.print_matrix) <= self.cur_matrix_pos + 1:
            self.cur_matrix_pos = 0
        else: self.cur_matrix_pos += 1


   