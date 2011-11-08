#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import re

class Checker:

  def load_voc(self,filename):
    f = open(filename,'rU')
    lines = f.readlines()
    self.voc = []
    for line in lines:
      a = re.search('(.*)\xa4=\xa4(.*)',line)
      if a:
        self.voc.append((a.group(1).decode('windows-1250'),a.group(2).decode('windows-1250')))
    f.close()
    return self.voc
  
  def load_colnames(self,filename):
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

  def check(self,guessed,shouldbe):
    translations = [('ą','a'),('ć','c'),('ę','e'),('ł','l'),('ń','n'),('ó','o'),('ś','s'),('ź','z'),('ż','z')]
    for pol,lat in translations:
      guessed = guessed.replace(pol,lat)
      shouldbe = shouldbe.replace(pol,lat)
    if guessed.lower() == shouldbe.lower():
      return True
    return False

  def __init__(self,filename):
    self.load_voc(filename)
    (self.col1,selfcol2)=self.load_colnames(filename)
