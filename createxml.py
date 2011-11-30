#!/usr/bin/env python
#-*- coding: utf-8 -*-

from xml.dom.minidom import Document
from xml.dom import minidom

class HandleXML:

  def create_xml(self, settings = None, filename='settings.xml'):
    '''Sets values or creates default settings.xml file, calls read_xml()'''
    doc = Document()

    sett = doc.createElement('settings')
    doc.appendChild(sett)

    ignore = doc.createElement('ignore')
    sett.appendChild(ignore)

    ignores=[]
    if not settings:
      settings = {'case':1,'accents':1,'whitespaces':1}
    for index,key in enumerate(settings.keys()):
      ignores.append(doc.createElement(key))
      ignores[index].setAttribute('value',str(self.str2bool(settings[key])))
      ignore.appendChild(ignores[index])

    sounds = doc.createElement('sounds')
    sett.appendChild(sounds)

    good = doc.createElement('good')
    good.setAttribute('filename','path')
    sounds.appendChild(good)

    bad= doc.createElement('bad')
    bad.setAttribute('filename','path')
    sounds.appendChild(bad)

    finish = doc.createElement('finish')
    finish.setAttribute('filename','path')
    sounds.appendChild(finish)

    end = doc.createElement('end')
    end.setAttribute('filename','path')
    sounds.appendChild(end)

    f = open(filename,'w')
    f.write(doc.toprettyxml(indent='  '))
    f.close()
    return self.read_xml()
    
  def read_xml(self, filename='settings.xml'):
    '''Reads file, gets values and returns the settings'''
    import xml.parsers.expat    # cause i need to handle exception
    try:
      doc = minidom.parse(filename)
    except IOError as e:
      print 'There is no settings.xml! Making a new one'
      return 0
    except xml.parsers.expat.ExpatError as e:
      print 'It\'s not a proper xml file I suppose. Making a new one'
      return 0
      
    dictionary = {'case':None,'accents':None,'whitespaces':None}
    for key in dictionary.keys():     #find tag get attribute for key convert to int
      dictionary[key] = int(doc.getElementsByTagName(key)[0].getAttribute('value'))
    return dictionary 

  def str2bool(self, v):
    '''Stupid function that converts True And False to 1 and 0, I need this to convert
strings to 1 and 0 value for attributes. Probably there's a better way
to do this'''

    if v:
      return 1
    else:
      return 0
