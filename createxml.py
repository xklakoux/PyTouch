#!/usr/bin/env python
#-*- coding: utf-8 -*-

from xml.dom.minidom import Document
from xml.dom import minidom

class HandleXML:

  def create_xml(self, settings = None, filename='settings.xml'):
    doc = Document()

    sett = doc.createElement('settings')
    doc.appendChild(sett)

    ignore = doc.createElement('ignore')
    sett.appendChild(ignore)


    if settings:
      ignores=[]
      for index,key in enumerate(settings.keys()):
        ignores.append(doc.createElement(key))
        ignores[index].setAttribute('value',str(self.str2bool(settings[key])))
        ignore.appendChild(ignores[index])
    else:
      case = doc.createElement('case')
      case.setAttribute('value','1')
      ignore.appendChild(case)

      accents = doc.createElement('accents')
      accents.setAttribute('value','1')
      ignore.appendChild(accents)

      white = doc.createElement('whitespaces')
      white.setAttribute('value','1')
      ignore.appendChild(white)

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

    f = open('settings.xml','w')
    f.write(doc.toprettyxml(indent='  '))
    f.close()
    
  def read_xml(self, filename='settings.xml'):
    doc = minidom.parse('settings.xml')
    dictionary = {'case':None,'accents':None,'whitespaces':None}
    for key in dictionary.keys():     #find tag get attribute for key convert to int
      dictionary[key] = int(doc.getElementsByTagName(key)[0].getAttribute('value'))
    return dictionary 

  def str2bool(self, v):
    if v:
      return 1
    else:
      return 0
