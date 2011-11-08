#!/usr/bin/env python
#-*- coding: windows-1250 -*-
  
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gen


class LoadTest():
  def check_sb(self,cell,path,model):
    print str(cell)
    print str(path)
    model[path][0] = not model[path][0]
    return 

  def start_cb(self,widget,data=None):
    self.window.hide()
  def load_cb(self,widget,data=None):
    dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.set_modal(True)

    filter = gtk.FileFilter()
    filter.set_name("Pytacz Master Text Files")
    filter.add_pattern("*.txt")
    dialog.add_filter(filter)

    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)


    response = dialog.run()
    if response == gtk.RESPONSE_OK:
      self.filename = dialog.get_filename()
      self.entry.set_text(self.filename) #show only the filename
      self.words = gen.Checker(self.filename)
      if not 'liststore' in vars(self):
        self.make_table(self.words.voc)
      else:
        self.liststore.clear()
        for (first,two) in self.words.voc:
          self.liststore.append((True,first,two))
      self.startbutton.set_sensitive(True)
    elif response == gtk.RESPONSE_CANCEL:
      self.filename = None
    dialog.destroy()
  def evented(self,widget,event):
    if gtk.gdk.keyval_name(event.keyval) == 'space':
      pass
      pass
      #self.check_sb(self.celltoggle,1,self.liststore)
  def make_table(self,words):
    self.liststore = gtk.ListStore(gobject.TYPE_BOOLEAN,gobject.TYPE_STRING,gobject.TYPE_STRING)

    for (first,two) in words:
      self.liststore.append((True,first,two))

    self.treeview = gtk.TreeView(self.liststore)
    self.treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
    self.celltext = gtk.CellRendererText() 
    self.celltext2 = gtk.CellRendererText()
    self.celltoggle = gtk.CellRendererToggle()
    self.celltoggle.set_property('activatable',True)
    self.celltoggle.connect('toggled',self.check_sb,self.liststore)
    self.treeview.set_events(gtk.gdk.KEY_PRESS_MASK)
    self.treeview.connect('key_press_event',self.evented)

    self.tvcolumn1 = gtk.TreeViewColumn('Check')
    self.tvcolumn1.pack_start(self.celltoggle,True)
    self.tvcolumn1.add_attribute(self.celltoggle,'active',0)

    self.treeview.append_column(self.tvcolumn1)
    self.tvcolumn2 = gtk.TreeViewColumn(self.words.col1)
    self.tvcolumn2.pack_start(self.celltext,True)
    self.tvcolumn2.add_attribute(self.celltext,'text',1)

    self.treeview.append_column(self.tvcolumn2)
    self.tvcolumn3 = gtk.TreeViewColumn(self.words.col2)
    self.tvcolumn3.pack_start(self.celltext2,True)
    self.tvcolumn3.add_attribute(self.celltext2,'text',2)
    self.treeview.append_column(self.tvcolumn3)
    self.scrolled = gtk.ScrolledWindow()
    self.scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.scrolled.add_with_viewport(self.treeview)
    self.window.vbox.pack_start(self.scrolled,True,True,10)
    self.window.show_all()

  def __init__(self,words):

    self.filename = ''

    self.window = gtk.Dialog()
    self.window.set_modal(True)
    self.window.set_size_request(500,500)
    self.window.set_border_width(10)
    self.window.set_resizable(False)
    self.window.set_title('Editor')
    self.window.connect('destroy',lambda wid:self.window.hide())
    self.window.connect('delete_event',lambda a1,a2:self.window.hide())
    

    box = gtk.HBox(False,0)
    self.window.vbox.pack_start(box,False,False,10)
    self.entry = gtk.Entry()
    self.entry.set_sensitive(False)
    self.entry.set_alignment(1.0)
    self.entry.show()
    
    self.loadbutton = gtk.Button('Load test')
    self.loadbutton.connect('clicked',self.load_cb)
    self.loadbutton.show()
    
    box.pack_start(self.entry,True,True,10)
    box.pack_end(self.loadbutton,False,False,10)

    self.startbutton = gtk.Button('Start Test')
    self.startbutton.connect('clicked',self.start_cb)
    self.startbutton.set_sensitive(False)
    self.startbutton.show()
    
    self.window.vbox.pack_start(self.startbutton,False,False,10)
    box.show()
    
    if words:
      self.make_table(words)



