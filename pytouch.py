#!/usr/bin/env python
#-*- coding: windows-1250 -*-
u"""This is a clone of a freeware program 'Pytacz Master' written by kl4q"""

import pygtk
pygtk.require('2.0')
import gtk
import gen
import loadtest
import random
import os
import edit

class Base:

  def load_test_cb(self,widget,data=None):
    if not 'ltdialog' in vars(self):
      self.ltdialog = loadtest.LoadTest()
    self.ltdialog.window.run()
    if self.ltdialog.words.voc:
      self.oncemore.set_sensitive(True)
      self.finish.set_sensitive(True)
      self.begin()
    
  def load_test(self):
    pass 

  def begin(self):
    self.progressbar.set_fraction(0)
    self.good=0
    self.bad=0
    self.labelgood.set_text(str(self.good))          #delete old test remainders and put a new one
    self.labelbad.set_text(str(self.bad))
    self.guessed.set_sensitive(True)
    self.radio_button.set_sensitive(True)
    self.radio_button1.set_sensitive(True)
    self.checkbutton.set_sensitive(True)
    self.finish.set_sensitive(True)
    if os.name == 'nt':
      self.labeltest.set_text(self.ltdialog.filename.split("\\")[-1]) #show only the filename
    else:
      self.labeltest.set_text(self.ltdialog.filename.split("/")[-1]) #show only the filename
    self.wordsrev = []
    self.words = self.ltdialog.words
    self.wordslen = len(self.words.voc)
    self.label1.set_text(self.words.col1)
    self.label2.set_text(self.words.col2)
    self.start_test()

  def edit_callback(self,widget,data=None):
    editor = edit.Editor()

  def shut_down(self):
    self.guessed.set_sensitive(False)
    self.checkbutton.set_sensitive(False)
    #self.oncemore.set_sensitive(False)
    self.finish.set_sensitive(False)
    self.guessed.set_text('')
    self.showed.set_text('')
    self.progressbar.set_fraction(0)
    self.entryRem.set_text('-')
    #self.good=0
    #self.bad=0
    #self.labelgood.set_text(str(self.good))          #delete old test remainders and put a new one
    #self.labelbad.set_text(str(self.bad))
    self.radio_button.set_sensitive(False)
    self.radio_button1.set_sensitive(False)
    self.labelrem.set_text(str(len(self.words.voc)) + "("+ str(len(self.wordsrev)) +")")

  def start_test(self):
    self.labelrem.set_text(str(len(self.words.voc)) + "("+ str(len(self.wordsrev)) +")")
    self.labelrem.show()
    if not self.words.voc:      #if there are no more words
      self.shut_down()
      return 0;
    self.checked = random.choice(self.words.voc)
    self.ix = self.words.voc.index(self.checked)  #index number for future marking (complete, revision)
    self.showed.set_text(self.checked[self.mode])
    self.guessed.set_text('')
    self.guessed.grab_focus()
    self.guessed.show()
    self.showed.show()

  def sett_callback(self,widget,data=None):
    self.dialogsett = gen.DialogSett(self.settings)
    response = self.dialogsett.window.run()
    if response == gtk.RESPONSE_OK:
      self.settings['polish'] = self.dialogsett.polishbutton.get_active()
      self.settings['case'] = self.dialogsett.casebutton.get_active()
      self.settings['white'] = self.dialogsett.whitebutton.get_active()
    self.dialogsett.window.destroy()

  def its_done(self):
    if not len(self.words.voc):    #if there are no other words
      self.guessed.set_text('')
      self.showed.set_text('')
      self.showed.show()
      if len(self.wordsrev):      #if there are some words in revision
        self.words.voc = self.wordsrev
        self.wordsrev = []
        #here it should wait a while but it cant
      else:
        self.guessed.set_sensitive(False)
        #self.guessed.show()

  def check_callback(self,widget,data=None):
    if self.words.check(self.guessed.get_text(),self.words.voc[self.ix][self.mode-1], self.settings): #1 if self.mode is 0 and opposite
      self.words.voc.pop(self.ix)
      self.good+=1
      self.labelgood.set_text(str(self.good)) 
      self.entryRem.set_text('-')
      self.its_done()
    else:
      self.wordsrev.append(self.words.voc[self.ix])
      self.bad+=1
      self.labelbad.set_text(str(self.bad))
      self.wordslen+=1
      #self.labelbad.show()
      self.entryRem.set_text(self.wordsrev[-1][0] + " - " + self.wordsrev[-1][1])
    self.progressbar.set_fraction(float(self.good)/float(self.wordslen))
    #self.progressbar.show()
    #self.labelgood.show()
    #self.entryRem.show()
    self.start_test() 

  def finish_callback(self,widget,data=None):
    self.words.voc = []
    self.wordsrev = []
    self.shut_down()

  def oncemore_callback(self,widget,data=None):
    self.words.voc = [(two,three) for (one,two,three) in self.ltdialog.liststore if one==True]
    self.begin() 

  def radio_callback(self,widget,data=None):
    self.guessed.set_sensitive(True)
    self.showed.set_sensitive(False)
    self.guessed.grab_focus()
    self.mode=1
    self.start_test()

  def radio1_callback(self,widget,data=None):
    self.guessed,self.showed = self.showed,self.guessed
    self.guessed.set_sensitive(True)
    self.showed.set_sensitive(False)
    self.guessed.grab_focus()
    self.mode=0
    self.start_test()

  def __init__(self):
    self.settings = {'polish':True,'case':True,'white':True}
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_size_request(400,-1)
    self.window.set_border_width(10)
    self.window.set_resizable(False)
    self.window.set_title('PyTouch')
    self.window.connect('destroy',lambda wid: gtk.main_quit())
    self.window.connect('delete_event',lambda a1,a2:gtk.main_quit())
    mainbox=gtk.VBox(False,0)
    box1=gtk.HBox(False,0)
    box1.set_border_width(2)

    self.tooltips = gtk.Tooltips()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/open.png')
    image.show()
    button.connect('clicked',self.load_test_cb)
    box1.pack_start(button,False,False,0)
    button.add(image)
    self.tooltips.set_tip(button,"Load test")
    button.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/edit.png')
    image.show()
    button.connect('clicked',self.edit_callback)
    box1.pack_start(button,False,False,0)
    button.add(image)
    self.tooltips.set_tip(button,"Test editor")
    button.show()

    button = gtk.Button()
    image = gtk.Image()
    image.set_from_file('gfx/sett.png')
    image.show()
    button.connect('clicked',self.sett_callback)
    box1.pack_start(button,False,False,0)
    button.add(image)
    self.tooltips.set_tip(button,"Settings")
    button.show()

    box1.show()

    separator = gtk.HSeparator()
    separator.show()
    mainbox.pack_start(box1,False,False,0)
    mainbox.pack_start(separator,False,False,5)

    self.labeltest = gtk.Label('No test set');
    self.labeltest.show()
    mainbox.pack_start(self.labeltest,False,True,0)

    self.progressbar=gtk.ProgressBar(adjustment=None)
    self.progressbar.set_fraction(0)
    self.progressbar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
    self.progressbar.set_text('Progress you\'ve made')
    self.progressbar.show()
    separator = gtk.HSeparator()
    separator.show()
    mainbox.pack_start(self.progressbar,False,True,0)
    mainbox.pack_start(separator,False,False,5)
   
    boxHFC=gtk.HBox(False,0)

    boxFC=gtk.VBox(False,0)
    boxFC.show()

    self.label1 = gtk.Label('First Column');
    self.label1.show()
    boxFC.pack_start(self.label1,False,True,0)
    entryFC = gtk.Entry(max=0)
    entryFC.connect('activate',self.check_callback)
    entryFC.set_max_length(100)
    entryFC.set_sensitive(False)
    entryFC.show()
    boxFC.pack_start(entryFC,False,True,0)
    boxHFC.show()

    self.radio_button = gtk.RadioButton(None)
    self.radio_button.connect('toggled',self.radio_callback)
    self.mode = 1
    self.radio_button.set_sensitive(False)
    self.radio_button.show()
    self.tooltips.set_tip(self.radio_button,"Ask me about this column")
    boxHFC.pack_start(boxFC, True, True, 0)
    boxHFC.pack_end(self.radio_button, False, False, 0)

    boxHSC=gtk.HBox(False, 0)
    boxSC=gtk.VBox(False, 0)
    boxSC.show()
    boxHSC.show()
    self.label2= gtk.Label('Second Column');
    self.label2.show()
    boxSC.pack_start(self.label2,False, True, 0)
    entrySC = gtk.Entry(max=0)
    entrySC.connect('activate', self.check_callback)
    entrySC.set_max_length(100)
    entrySC.set_sensitive(False)
    entrySC.show()
    boxSC.pack_start(entrySC, False, True,0)
    self.guessed = entryFC
    self.showed = entrySC
    self.radio_button1 = gtk.RadioButton(self.radio_button)
    self.radio_button1.connect('toggled',self.radio1_callback)
    self.radio_button1.set_sensitive(False)
    self.radio_button1.show()
    self.tooltips.set_tip(self.radio_button1,"Ask me about this column")
    boxHSC.pack_start(boxSC,True,True,0)
    boxHSC.pack_end(self.radio_button1, False, False, 0)
    
    mainbox.pack_start(boxHFC,False,False,5)
    mainbox.pack_start(boxHSC,False,False,5)
    
    box3 = gtk.HBox(False,0)
    checkbox = gtk.HBox(True,5)
    checkbox.show()

    self.checkbutton = gtk.Button('    Check    ')
    checkbox.pack_start(self.checkbutton,False,False,0)
    self.checkbutton.set_sensitive(False)
    self.checkbutton.connect('clicked',self.check_callback)
    mainbox.pack_start(checkbox,False,False,0) 
    self.checkbutton.show()

    self.oncemore = gtk.Button()
    self.oncemore.set_sensitive(False)
    image = gtk.Image()
    image.show()
    image.set_from_file('gfx/oncemore.png')
    self.oncemore.connect('clicked',self.oncemore_callback)
    self.oncemore.add(image)
    box3.pack_end(self.oncemore,False,False,0)
    self.tooltips.set_tip(self.oncemore,"Restart")
    self.oncemore.show()

    self.finish = gtk.Button()
    self.finish.set_sensitive(False)
    self.tooltips.set_tip(self.finish,"Finish")
    self.finish.show()
    image = gtk.Image()
    image.show()
    image.set_from_file('gfx/finish.png')
    self.finish.connect('clicked',self.finish_callback)
    self.finish.add(image)
    box3.pack_end(self.finish,False,False,0)
    box3.show()
    mainbox.pack_start(box3,False,False,0)
    
    label = gtk.Label('REMEMBER');
    label.show()
    mainbox.pack_start(label,False,True,0)
    self.entryRem = gtk.Entry(max=0)
    self.entryRem.set_max_length(100)
    self.entryRem.set_editable(False)
    self.entryRem.set_alignment(0.5)
    self.entryRem.insert_text('-')
    self.entryRem.set_sensitive(False)
    self.entryRem.show()
    mainbox.pack_start(self.entryRem,False,False,0)

    separator = gtk.HSeparator()
    mainbox.pack_start(separator,False,False,20)
    separator.show()

    box4 = gtk.HBox(True,5)
    eventbox = gtk.EventBox()
    eventbox.show()
    eventbox.modify_bg(gtk.STATE_NORMAL,eventbox.get_colormap().alloc_color('green'))
    label = gtk.Label('Correct')
    eventbox.add(label)
    label.show()
    box4.pack_start(eventbox,False,True,0)

    eventbox = gtk.EventBox()
    eventbox.show()
    eventbox.modify_bg(gtk.STATE_NORMAL,eventbox.get_colormap().alloc_color('green'))
    self.good = 0
    self.labelgood = gtk.Label('0')
    eventbox.add(self.labelgood)
    self.labelgood.show()
    box4.pack_start(eventbox,False,True,4)

    eventbox = gtk.EventBox()
    eventbox.show()
    eventbox.modify_bg(gtk.STATE_NORMAL,eventbox.get_colormap().alloc_color('red'))
    label = gtk.Label('Incorrect')
    label.show()
    eventbox.add(label)
    box4.pack_end(eventbox,False,True,4)

    eventbox = gtk.EventBox()
    eventbox.show()
    self.bad = 0
    self.labelbad = gtk.Label('0')
    self.labelbad.show()
    eventbox.modify_bg(gtk.STATE_NORMAL,eventbox.get_colormap().alloc_color('red'))
    box4.pack_end(eventbox,False,True,0)
    eventbox.add(self.labelbad)

    box4.show()
    mainbox.pack_start(box4,False,False,10)
    
    box = gtk.HBox(True,0)
    label = gtk.Label('Remain')
    label.show()
    box.pack_start(label,False,False,0)
    self.labelrem = gtk.Label('0(0)')
    self.labelrem.show()
    box.pack_end(self.labelrem,False,False,0)
    box.show()

    mainbox.pack_start(box,False,False,0)

    self.window.add(mainbox)
    

    mainbox.show()
    self.window.show() 
    #self.words=[]

def main():
    gtk.main()
    return 0

if __name__ == '__main__':
  Base()
  main()
