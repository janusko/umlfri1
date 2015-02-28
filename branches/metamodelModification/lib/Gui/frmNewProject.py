from lib.Depend.gtk2 import gtk, pango

from lib.Drawing.PixmapImageLoader import PixmapFromPath

import common
from lib.consts import PROJECT_CLEARXML_EXTENSION
from lib.Distconfig import TEMPLATES_PATH, IMAGES_PATH, USERDIR_PATH

import pango
import os
import os.path
import gobject
import zipfile
from common import event

class CfrmNewProject (common.CWindow):
    name = 'frmNewProject'

    glade = 'project.glade'

    widgets = ("ivNewProject", "twNewProject", "drawingarea")

    COL_NAME, \
    COL_ICON, \
    COL_OBJ = range (3)

    def __init__(self, app, wTree):
        common.CWindow.__init__ (self, app, wTree)

        self.ivNewModel = gtk.ListStore (
            gobject.TYPE_STRING,
            gtk.gdk.Pixbuf,
            gobject.TYPE_PYOBJECT
        )
        self.ivNewProject.set_model (self.ivNewModel)
        self.ivNewProject.set_text_column (self.COL_NAME)
        self.ivNewProject.set_pixbuf_column (self.COL_ICON)

        self.__createTextTags ()

    def __GetIcon (self, filename):
        if not os.path.isfile(filename):
            return gtk.gdk.pixbuf_new_from_file(os.path.join(IMAGES_PATH, 'default_icon.png'))
        f = os.tempnam()
        ext = filename.split('.')
        ext.reverse()

        if (("."+ext[0]) != PROJECT_CLEARXML_EXTENSION):
            try:
                z = zipfile.ZipFile(filename)
                for i in z.namelist():
                    if i in ('icon.png', 'icon.gif', 'icon.jpg', 'icon.ico', 'icon.png'):
                        file(f, 'wb').write(z.read(i))
                        ret = gtk.gdk.pixbuf_new_from_file(f)
                        os.unlink(f)
                        return ret
            except zipfile.BadZipfile:
                pass

        return gtk.gdk.pixbuf_new_from_file(os.path.join(IMAGES_PATH, 'default_icon.png'))

    def __createTextTags (self):
        buffer = self.twNewProject.get_buffer ()
        buffer.create_tag (
            "heading",
            weight=pango.WEIGHT_BOLD,
            size=15*pango.SCALE
        )
        buffer.create_tag (
            "italic",
            style=pango.STYLE_ITALIC
        )

    def __updateDescription (self, template):
        metamodel = self.application.GetAddonManager ().GetAddon (
            template.GetMetamodelUri()
        )
        buffer = self.twNewProject.get_buffer ()
        buffer.set_text ("")
        iter = buffer.get_iter_at_offset (0)
        buffer.insert_with_tags_by_name (
            iter,
            metamodel.GetName (),
            "heading"
        )
        buffer.insert_with_tags_by_name (
            iter,
            "\nMetamodel version: " + metamodel.GetVersionString() + "\n",
            "italic"
        )
        buffer.insert (
            iter,
            metamodel.GetDescription ()
        )


    @event("ivNewProject", "item-activated")
    def on_ivNewProject_item_activated (self, widget, path):
        self.form.response (gtk.RESPONSE_OK)

    @event("ivNewProject", "selection-changed")
    def on_ivNewProject_sel_changed (self, widget):
        selection = widget.get_selected_items ()
        if selection:
            model = widget.get_model ()
            iter = selection[0]
            self.__updateDescription (model[iter][self.COL_OBJ])


    @event("drawingarea", "expose-event")
    def on_drawingarea_expose(self, widget, event):
        context = widget.window.cairo_create()
        context.rectangle(event.area.x, event.area.y,
            event.area.width, event.area.height)
        #context.clip()
        # get style
        style = widget.get_style().bg
        bg = style[gtk.STATE_SELECTED]
        if bg == None or type(bg) != gtk.gdk.Color:
            fg = gtk.gdk.Color(65535, 65535, 65535)
        style = widget.get_style().fg
        fg = style[gtk.STATE_SELECTED]
        if fg == None or type(fg) != gtk.gdk.Color:
            bg = gtk.gdk.Color(0, 0, 0)
        context.set_source_color(bg)
        context.fill()
        # draw text
        layout = widget.create_pango_layout('Create new project')
        layout.set_font_description(pango.FontDescription(
            "Sans Serif Bold 20"))
        context.set_source_color(fg)
        context.move_to(5, 5)
        context.show_layout(layout)

    def ShowDialog (self, parent):
        self.form.set_transient_for (parent.form)
        self.ivNewModel.clear ()
        for template in self.application.GetTemplateManager ().GetAllTemplates ():
            iter = self.ivNewModel.append ()
            self.ivNewModel.set (
                iter,
                0, template.GetName (),
                2, template
            )
            if template.GetIcon () is not None:
                self.ivNewModel.set (
                iter,
                1, PixmapFromPath (template.GetStorage (),
                    template.GetIcon())
                )
        try:
            while True:
                run  = self.form.run ()
                if run != gtk.RESPONSE_OK:
                    self.form.hide ()
                    return None, False
                tmp = self.ivNewProject.get_selected_items ()
                if tmp:
                    iter = self.ivNewModel.get_iter (tmp[0])
                    return self.ivNewModel.get (iter, 2)[0], None
        finally:
            self.form.hide ()