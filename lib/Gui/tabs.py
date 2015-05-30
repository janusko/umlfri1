from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

from common import CWidget
from common import event
from lib.Drawing.PixmapImageLoader import PixmapFromPath

class CTabs(CWidget):
    name = 'nbTabs'
    widgets = ('nbTabs', 'tbDrawingArea',
                #Context menu
                'mnuTab', 'mnuTabExportSVG', 'mnuTabPages_menu', 'mnuTabCloseDiagram', 'mnuTabCloseAllDiagram',
                'mnuTabShowInProjectView',)
    
    __gsignals__ = {
        'change_current_page':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) 
            ),
        'drawing-area-set-focus': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'export-svg-from-TabMenu': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'show-diagram-in-project': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    }
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)

        self.mnuTabExportSVG.set_sensitive(False)
        self.mnuTabCloseDiagram.set_sensitive(False)
        self.mnuTabCloseAllDiagram.set_sensitive(False)
        self.mnuTabShowInProjectView.set_sensitive(False)
        sp = self.nbTabs.get_nth_page(0)
        sp.set_data("startpage", True)
        splbl = self.nbTabs.get_tab_label(sp)
        self.nbTabs.remove_page(0)
        self.__AddNbPage(None, None, sp, label = splbl)
        self.__RefreshEnable()
    
    def __RefreshEnable(self):
        sp = self.nbTabs.get_nth_page(self.__StartPageIndex())
        if self.nbTabs.get_n_pages() == 1:
            sp.show()
        splbl = self.nbTabs.get_tab_label(sp)
        splbl.get_children()[-1].set_sensitive(self.nbTabs.get_n_pages() > 1)

    def __PagesGenerator(self):
        '''
        Yield generator for Notebook's pages.
        :return:
        '''
        for i in range(self.nbTabs.get_n_pages()):
            yield (i, self.nbTabs.get_nth_page(i))

    def __StartPageIndex(self):
        """
        Return index of start page.
        :return: page
        """
        for i, page in self.__PagesGenerator():
            if page.get_data("startpage") is True:
                return i

    def __AddNbPage(self, diagram, pixbuf, page, label = None):
        hboxbut = gtk.HBox(spacing = 3)
        hboxbut.show()
        
        if pixbuf is not None:
            img = gtk.Image()
            img.set_from_pixbuf(pixbuf)
            img.show()
        
        if label is None:
            label = gtk.Label(diagram.GetName())
            label.show()
        
        button = gtk.Button()
        image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_SMALL_TOOLBAR)       
        image.show()
        button.add(image)
        button.set_relief(gtk.RELIEF_NONE)
        button.show()
        button.connect("clicked", self.on_button_click, page)
        
        if pixbuf is not None:
            hboxbut.add(img)
        hboxbut.add(label)
        hboxbut.add(button)
        self.nbTabs.append_page(page, hboxbut)
        self.nbTabs.set_tab_reorderable(page, True)

    def AddTab(self, diagram):
        for i, page in self.__PagesGenerator():
            if page.get_data("diagram") == diagram:
                self.nbTabs.set_current_page(i)
                return

        page = gtk.HBox()
        page.show()
        page.set_data("diagram", diagram)
        
        self.__AddNbPage(
            diagram,
            PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), diagram.GetType().GetIcon()),
            page)
       
        self.nbTabs.set_current_page(-1)
        self.__RefreshEnable()
    
    def Show(self):
        #self.nbTabs.show() # this wil show/hide the whole notebook
        self.nbTabs.set_property('show-tabs', True)
    
    def Hide(self):
        #self.nbTabs.hide() # this wil show/hide the whole notebook
        self.nbTabs.set_property('show-tabs', False)
    
    def SetVisible(self, value):
        if value:
            self.Show()
        else:
            self.Hide()
    
    def on_button_click(self, widget, page):
        self.CloseTab(self.nbTabs.page_num(page))

    @event("nbTabs", "switch-page")
    def on_change_current_page(self, notebook, page, page_num):
        if self.tbDrawingArea.get_parent():
            self.tbDrawingArea.get_parent().remove(self.tbDrawingArea)

        page = self.nbTabs.get_nth_page(page_num)
        if page.get_data("startpage") is True:
            self.emit("change_current_page", None)
            self.mnuTabExportSVG.set_sensitive(False)
            self.mnuTabCloseDiagram.set_sensitive(False)
            self.mnuTabShowInProjectView.set_sensitive(False)
            if self.nbTabs.get_n_pages() == 1:
                self.mnuTabCloseAllDiagram.set_sensitive(False)
            for chld in page.get_children():
                chld.show()
        else:
            diagram = page.get_data("diagram")
            self.application.GetOpenedDrawingAreas().GetDrawingArea(diagram).GetSelection().DeselectAll()
            page.pack_start(self.tbDrawingArea)
            self.emit("change_current_page", diagram)
            self.mnuTabExportSVG.set_sensitive(True)
            self.mnuTabCloseDiagram.set_sensitive(True)
            self.mnuTabCloseAllDiagram.set_sensitive(True)
            self.mnuTabShowInProjectView.set_sensitive(True)
            for chld in self.nbTabs.get_nth_page(self.__StartPageIndex()).get_children():
                chld.hide()

    def IsStartPageActive(self):
        return self.nbTabs.get_current_page() == self.__StartPageIndex()

    def CloseTab(self, page_num):
        page = self.nbTabs.get_nth_page(page_num)
        if page.get_data("startpage") is True:
            page.hide()
        else:
            if page_num == self.nbTabs.get_current_page() and self.tbDrawingArea.get_parent():
                self.tbDrawingArea.get_parent().remove(self.tbDrawingArea)
            self.nbTabs.remove_page(page_num)
        self.__RefreshEnable()

    def CloseTabByDiagram(self, diagram):
        for i, page in self.__PagesGenerator():
            _diagram = page.get_data("diagram")
            if _diagram == diagram:
                if i == self.nbTabs.get_current_page() and self.tbDrawingArea.get_parent():
                    self.tbDrawingArea.get_parent().remove(self.tbDrawingArea)
                self.nbTabs.remove_page(i)
        self.__RefreshEnable()

    def CloseCurrentTab(self):
        self.CloseTab(self.nbTabs.get_current_page())
    
    def NextTab(self):
        self.nbTabs.set_current_page(self.nbTabs.get_current_page()+1 % self.nbTabs.get_n_pages())
        if self.nbTabs.get_nth_page(self.nbTabs.get_current_page()).get_data("startpage") is not True:
            self.emit("drawing-area-set-focus")
    
    def PreviousTab(self):
        self.nbTabs.set_current_page(self.nbTabs.get_current_page()-1 % self.nbTabs.get_n_pages())
        if self.nbTabs.get_nth_page(self.nbTabs.get_current_page()).get_data("startpage") is not True:
            self.emit("drawing-area-set-focus")

    def CloseAll(self):
        if self.tbDrawingArea.get_parent():
            self.tbDrawingArea.get_parent().remove(self.tbDrawingArea)
        for i in range(self.nbTabs.get_n_pages()):
            self.CloseTab(i)

    def SetStartPageAsCurrentPage(self):
        spi = self.__StartPageIndex()
        self.nbTabs.get_nth_page(spi).show()
        self.nbTabs.set_current_page(spi)

    def on_mnuTab_activate(self, widget, index):
        '''
        It's executed after clicked on radio button.
        :param widget:
        :param index: index of page
        :return:
        '''
        if self.nbTabs.get_current_page() != index:
            self.nbTabs.set_current_page(index)

    @event("nbTabs","button-press-event")
    def button_clicked(self, widget, event):
        if event.button == 3:
            for i in self.mnuTabPages_menu.get_children():
                self.mnuTabPages_menu.remove(i)

            for i, page in self.__PagesGenerator():
                name = page.get_data("diagram").GetName() if page.get_data("diagram") is not None else "Start Page"
                mi = gtk.RadioMenuItem(None, name)
                if i > 0:
                    mi.set_group(self.mnuTabPages_menu.get_children()[0])
                mi.show()
                mi.connect("toggled", self.on_mnuTab_activate, i)
                self.mnuTabPages_menu.append(mi)
            self.mnuTabPages_menu.get_children()[self.nbTabs.get_current_page()].set_property("active", True)
            self.mnuTab.popup(None, None, None, event.button, event.time)
    
    @event("mnuTabCloseDiagram", "activate")
    def on_mnuTabCloseDiagram_activate(self, menuItem):
        self.CloseTab(self.nbTabs.get_current_page())
    
    @event("mnuTabCloseAllDiagram", "activate")
    def on_mnuTabCloseAllDiagram_activate(self, menuItem):
        self.CloseAll()
    
    @event("mnuTabShowInProjectView","activate")
    def on_mnuTabShowInProjectView_activate(self, menuItem):
        diagram = self.nbTabs.get_nth_page(self.nbTabs.get_current_page()).get_data("diagram")
        self.emit('show-diagram-in-project', diagram)

    @event("mnuTabExportSVG", "activate")
    def on_mnuTabExportSVG_activate(self, menuItem):
        if self.nbTabs.get_current_page() == self.__StartPageIndex():
            return
        else:
            self.emit("export-svg-from-TabMenu")
    
    @event('application.bus', 'diagram-changed')
    def DiagramChanged(self, bus, params):
        # TODO nezistil som aky ma zmysel tato metoda
        for obj, path in params:
            if path and obj in self.diagrams:
                self.labels[id(obj)].set_text(obj.GetName())
