#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import urllib
import re
import random

class Checker:
  '''This class contains function for most operations you do on the words,
including loading files, checking correction, fetching them from internet'''

  def load_voc(self,filename):
    '''Loads vocabulary'''
    if filename == 'Internet':    #vocabulary from internet
      self.voc = self.fetch() 
      self.col1 = 'English'
      self.col2 = 'Polish'
      return
    elif not filename:            #nothing happened
      self.voc = []
      self.col1 = 'First Column'
      self.col2 = 'Second Column'
      return
    f = open(filename,'rU')
    lines = f.readlines()
    for line in lines:
      a = re.search('(.*)\xa4=\xa4(.*)',line)
      if a:
        self.voc.append((a.group(1).decode('windows-1250'),a.group(2).decode('windows-1250')))
    f.close()
    self.load_colnames(filename)
  
  def load_colnames(self,filename):
    '''Loads column names if you specified any'''
    f = open(filename,'rU')
    lines = f.readlines()
    i=0
    for line in lines:
      if line == '[Kolumny]\n':
        self.col1 = lines[i+1][2:-1].decode('windows-1250')
        self.col2 = lines[i+2][2:-1].decode('windows-1250')
        f.close()
        return (self.col1,self.col2)
      i+=1
    f.close()
    return (None,None)

  def check(self,guessed,shouldbe,settings):
    u'''Checks if the answer is correct'''
    translations = [('ą','a'),('ć','c'),('ę','e'),('ł','l'),('ń','n'),('ó','o'),('ś','s'),('ź','z'),('ż','z'),\
    ('Ą','A'),('Ć','C'),('Ę','E'),('Ł','L'),('Ń','N'),('Ó','O'),('Ś','S'),('Ź','Z'),('Ż','Z')]
    if settings['accents'] == True:               #polish signs don't matter
      for pol,lat in translations:
        guessed = guessed.replace(pol,lat)
        shouldbe = shouldbe.replace(pol,lat)
    if settings['case'] == True:               #case doesn't matter
      guessed = guessed.lower()
      shouldbe = shouldbe.lower()
    if settings['whitespaces'] == True:               #white signs don't matter
      ' '.join(guessed.split())
      ' '.join(shouldbe.split())
    if guessed == shouldbe:
      return True
    return False


  def fetch(self):
    u'''Fetches 20 words from www.ang.pl''' 
    fromweb=[]
    while len(fromweb)<20:
      a = random.randint(1,3000)
      f = urllib.urlopen('http://www.ang.pl/wotd/archiwum/%d' % a)
      lines = f.readlines()
      for (ind,line) in enumerate(lines):
        solution = re.search('<b>WORD OF THE DAY</b>',line)
        if solution:
          solution = re.search('<b>(.+)</b>',lines[ind+4])
          if not solution:
            continue
          one = solution.group(1)
          solution = re.search('<b>(.+)</b>',lines[ind+17])
          if not solution:
            continue
          two = solution.group(1)
          fromweb.append((one,two))
        else:
          continue
    return fromweb 

  def __init__(self,filename):
    self.voc = []
    self.load_voc(filename)
    

class DialogSett:
  '''A Class to handle Settings Dialog'''

  def __init__(self,state):
    self.window = gtk.Dialog('Settings',None,gtk.DIALOG_MODAL,(gtk.STOCK_OK,gtk.RESPONSE_OK))
    self.window.connect('destroy',lambda hid:self.window.hide())
    self.window.connect('delete_event',lambda hid1,hid2:self.window.hide())
    self.window.set_border_width(10)

    self.accentsbutton = gtk.CheckButton('Ignore polish signs')
    self.accentsbutton.set_active(state['accents'])
    self.accentsbutton.show()
    self.window.vbox.pack_start(self.accentsbutton, False,False,0)
    self.casebutton = gtk.CheckButton('Ignore letter case')
    self.casebutton.set_active(state['case'])
    self.casebutton.show()
    self.window.vbox.pack_start(self.casebutton,False,False,0)
    self.whitebutton = gtk.CheckButton('Ignore Whitespaces')
    self.whitebutton.set_active(state['whitespaces'])
    self.whitebutton.show()
    self.window.vbox.pack_start(self.whitebutton,False,False,0)
    
