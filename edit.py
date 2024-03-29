#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gen
import gobject


class Editor:
  '''This class calls a window with editor for creating and editing new 
tests'''

  def changed_cb(self,widget):
    '''Handles multiple row selection'''
    self.rows = self.newselect
    self.newselect = self.selection.get_selected_rows()

  def make_table(self,words):
    '''Makes a new liststore'''
    if not 'liststore' in vars(self):
      self.liststore = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,\
      gobject.TYPE_STRING)
      
      #for (index,(first,two)) in enumerate(words):
        #self.liststore.append((index+1, first, two))
      self.iter = self.liststore.get_iter_first()
      self.treeview = gtk.TreeView(self.liststore)
      self.selection = self.treeview.get_selection()
      self.selection.set_mode(gtk.SELECTION_MULTIPLE)
      self.selection.connect('changed',self.changed_cb)
      self.newselect = []
      self.treeview.set_rubber_banding(True)
      self.celltext = gtk.CellRendererText() 
      self.celltext2 = gtk.CellRendererText()
      self.celltext3 = gtk.CellRendererText()
      #self.celltoggle.connect('toggled', self.check_cb, self.liststore)
      self.treeview.set_events(gtk.gdk.KEY_PRESS_MASK)
      self.treeview.connect('row_activated', self.edit_cb)

      self.tvcolumn1 = gtk.TreeViewColumn('Num')
      self.tvcolumn1.pack_start(self.celltext3, True)
      self.tvcolumn1.add_attribute(self.celltext3, 'text',0)

      self.treeview.append_column(self.tvcolumn1)
      self.tvcolumn2 = gtk.TreeViewColumn(self.words.col1)
      self.tvcolumn2.pack_start(self.celltext, True)
      self.tvcolumn2.add_attribute(self.celltext, 'text', 1)

      self.treeview.append_column(self.tvcolumn2)
      self.tvcolumn3 = gtk.TreeViewColumn(self.words.col2)
      self.tvcolumn3.pack_start(self.celltext2, True)
      self.tvcolumn3.add_attribute(self.celltext2, 'text', 2)
      self.treeview.append_column(self.tvcolumn3)
      self.scrolled = gtk.ScrolledWindow()
      self.scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      self.scrolled.add_with_viewport(self.treeview)
      self.mainvbox.pack_start(self.scrolled, True, True, 10)
      self.window.show_all()
    else:
      self.liststore.clear()
      if words:
        for (one,two) in words:
          self.liststore.append((True,one,two))
    #self.startbutton.set_sensitive(True)

  def new_test_cb(self, widget, data=None):
    '''Clears liststore'''
    if self.check_if_saved('opening new file'):
      return
    self.words.voc=[]
    self.liststore.clear()
    self.window.set_title('Test Editor')

    
  def save_as_cb(self, widget, data=None):
    '''Saves to a file with choosen filename'''
    dialog = gtk.FileChooserDialog("Save as..",None,gtk.FILE_CHOOSER_ACTION_SAVE,\
    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
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
    dialog.set_do_overwrite_confirmation(True)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
      self.filename = dialog.get_filename()
      self.save_cb(self.liststore,self.filename)
    elif response == gtk.RESPONSE_CANCEL:
      self.filename = None
    else:
      dialog.destroy()
      return True
    dialog.destroy()

  def save_cb(self, widget, data=None):
    if self.filename:
      self.window.set_title('{} - Test Editor'.format(self.filename))
      f = open(self.filename,'w')
      f.write('''[Informacje]
Autor=
Opis=
Ostatnia modyfikacja=

[Kolumny]
1=
2=

[Do zapamiętania]
Słówko1=Tak
Między=-
Słówko2=Tak

[Dane]\n'''.encode('windows-1250'))
      for (a,b,c) in self.liststore:
        f.write('{}\xa4=\xa4{}\r\n'.format(b.encode('windows-1250'),c.encode('windows-1250')))
      f.close()
      self.changed = False
    else:
      self.save_as_cb(self.treeview)

  def load_cb(self, widget, data=None):
    '''Loads new test from file'''
    if self.check_if_saved('opening new test'):
      return
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
      self.window.set_title('{} - Test Editor'.format(self.filename))
      self.words = gen.Checker(self.filename)
      self.liststore.clear()
      for (index, (one,two)) in enumerate(self.words.voc):
        self.liststore.append((index+1,one,two))
    elif response == gtk.RESPONSE_CANCEL:
      self.filename = None
    dialog.destroy()
    
  def check_correct(self,one,two):
    '''Check for duplicates'''
    for row in self.liststore:
      if (one,two) == (row[1],row[2]) or (one,two) == (row[1],row[2]):
        return False 
    return True

  def new_cb(self, widget, data=None):
    '''Makes a new record in liststore'''
    self.words_dialog(data[0],data[1])  
    self.dialog.set_default_response(gtk.RESPONSE_OK)
    response = self.dialog.run()
    if response == gtk.RESPONSE_OK:
      ent1 = self.entry1.get_text()
      ent2 = self.entry2.get_text()
      if not self.check_correct(ent1,ent2):
        message = gtk.MessageDialog(message_format='Duplicate error!',type=gtk.MESSAGE_WARNING,buttons=gtk.BUTTONS_OK)
        message.run()
        message.destroy()
        self.dialog.destroy()
        print ent1,ent2
        self.new_cb(None,(ent1,ent2))
        return 
      self.liststore.append((0,ent1,ent2))
      self.changed = True
      self.fix_numbers()
      self.dialog.destroy()
      self.new_cb(None,('',''))
    else:
      self.dialog.destroy()
    
  def fix_numbers(self):
    '''Special function to fix row ids'''
    for (index, value ) in enumerate(self.liststore):
      self.liststore[index][0]=index+1

  def edit_cb(self, widget, data=None,forcedbytreeview=None):
    '''Edit record'''
    (a,pathto) = self.selection.get_selected_rows()
    nr = pathto[0][0]
    self.words_dialog(self.liststore[nr][1],self.liststore[nr][2])
    self.dialog.set_default_response(gtk.RESPONSE_OK)
    response = self.dialog.run()
    if response == gtk.RESPONSE_OK:
      self.liststore[nr]=(self.liststore[nr][0],self.entry1.get_text(),self.entry2.get_text())
      self.changed = True
    self.dialog.destroy()

  def delete_cb(self, widget, data=None):
    '''Delete a record'''
    if self.selection.get_selected_rows()[1]:
      (a,pathto) = self.selection.get_selected_rows()
      self.liststore.remove(self.liststore.get_iter(pathto[0]))
      self.fix_numbers()
      self.changed = True

  def words_dialog(self, ent1, ent2):
    '''Makes a dialog where you can write your word pairs into'''
    self.dialog = gtk.Dialog(flags = gtk.DIALOG_MODAL,buttons=(gtk.STOCK_OK,gtk.RESPONSE_OK))
    self.dialog.set_default_response(gtk.RESPONSE_OK)
    self.dialog.set_modal(True)
    self.dialog.set_border_width(10)
    self.dialog.set_resizable(False)

    hbox = gtk.HBox(True,15)
    hbox.show()
    
    self.entry1 = gtk.Entry()
    hbox.pack_start(self.entry1)
    self.entry1.set_text(ent1)
    self.entry1.connect('activate',self.responseToDialog)
    self.entry1.show()

    self.entry2 = gtk.Entry()
    hbox.pack_start(self.entry2)
    self.entry2.set_text(ent2)
    self.entry2.connect('activate',self.responseToDialog)
    self.entry2.show()
    self.dialog.vbox.pack_start(hbox,False,False,0)

    return self.dialog
    
  def responseToDialog(self,widget,data=None):
    self.dialog.response(gtk.RESPONSE_OK)

  def check_if_saved(self,ending):
    '''A function that protects you from loosing new words'''
    if self.changed:
      message = gtk.MessageDialog(type=gtk.MESSAGE_WARNING,buttons=gtk.BUTTONS_YES_NO,message_format='Do you want to save your file before {}?'.format(ending))
      answer = message.run()
      if answer == gtk.RESPONSE_YES:
        if self.save_as_cb(None):
          message.destroy()
          return True
        message.destroy()
      elif answer == gtk.RESPONSE_NO:
        message.destroy()
      else:
        return True           #delete_event function required that
      return False
        
  def delete_event(self,widget,data=None):
    return self.check_if_saved('exit')


  def __init__(self):
     
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_size_request(500, 500)
    self.window.set_border_width(5)
    self.window.set_resizable(False)
    self.window.set_title('Test Editor')
    self.window.connect('destroy', lambda wig:self.window.destroy())
    self.window.connect('delete_event',self.delete_event) 
    
    self.tooltips = gtk.Tooltips()
    self.mainvbox = gtk.VBox(False,0)
    self.mainvbox.show()
    self.window.add(self.mainvbox)
    box1 = gtk.HBox(False, 0)
    self.mainvbox.pack_start(box1, False, False, 10)
    box1.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/new.png')
    image.show()
    button.connect('clicked',self.new_test_cb)
    box1.pack_start(button,False,False,2)
    button.add(image)
    self.tooltips.set_tip(button,"New test")
    button.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/open.png')
    image.show()
    button.connect('clicked',self.load_cb)
    box1.pack_start(button,False,False,2)
    button.add(image)
    self.tooltips.set_tip(button,"Load test")
    button.set_sensitive(True)
    button.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/save.png')
    image.show()
    button.connect('clicked',self.save_cb)
    box1.pack_start(button,False,False,2)
    button.add(image)
    self.tooltips.set_tip(button,"Save")
    button.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/saveas.png')
    image.show()
    button.connect('clicked',self.save_as_cb)
    box1.pack_start(button,False,False,2)
    button.add(image)
    self.tooltips.set_tip(button,"Save as...")
    button.show()

    separator = gtk.VSeparator()
    box1.pack_start(separator,False,False,2)
    separator.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/add.png')
    image.show()
    button.connect('clicked',self.new_cb,('',''))
    box1.pack_start(button,False,False,2)
    button.add(image)
    self.tooltips.set_tip(button,"New element")
    button.set_sensitive(True)
    button.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/editelement.png')
    image.show()
    button.connect('clicked',self.edit_cb)
    box1.pack_start(button,False,False,2)
    button.add(image)
    self.tooltips.set_tip(button,"Edit element")
    button.set_sensitive(True)
    button.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/del.png')
    image.show()
    button.connect('clicked',self.delete_cb)
    box1.pack_start(button,False,False,2)
    button.add(image)
    self.tooltips.set_tip(button,"Delete element")
    button.set_sensitive(True)
    button.show()

    self.window.show()
    self.filename = None
    self.words = gen.Checker(None)
    self.make_table(None)
    self.changed = False
