###############################################
###############################################
###############################################
#### This file has simple wrappers to qt4  ####
###############################################
###############################################
###############################################



from PyQt5 import QtGui,QtWidgets  # Import the PyQt5 module we'll need
from PyQt5.QtGui import QPixmap
#from PyQt5.QtCore import Signal
import sys  # We need sys so that we can pass argv to QApplication
import numpy as np
import os

from numpy import * # this may not be a good idea
from .qlinterface import running
from .debugging import holler

# This file holds our MainWindow and all interface related things
import interface # this file is generated by Qt-designer 

QtGui = QtWidgets
app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication


def get_failsafe(f,robust=True):
    """Return a function that if fails things do not break down"""
    def fout(*args,**kwargs):
        if not robust: return f()
        try: f()
        except: 
            if holler(): print("Something wrong happened")
            return None
    return fout



class App(QtGui.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in interface.py file automatically
        # It sets up layout and widgets that are defined
    def save_interface(self,**kwargs):
        save_interface(self,**kwargs)
    def run(self):
        self.show()  # Show the form
        app.exec_()  # and execute the app
    def get(self,*args,**kwargs):
        return get(*args,**kwargs)
    def set(self,*args):
        set_value(*args)
    def is_checked(self,*args,**kwargs):
        return is_checked(*args,**kwargs)
    def getbox(self,*args,**kwargs):
        return getbox(*args,**kwargs)
    def connect_clicks(self,ds,robust=True):
      """Connect the different functions"""
      ds2 = dict()
      for d in ds: 
          ds2[d] = get_failsafe(running(ds[d]),robust=robust) 
      for d in ds2:
          bu = getattr(self,d) # label in the interface
          fun = ds2[d] # function to call
          bu.clicked.connect(fun) # connect name to function


def main():
    global form
    form = App()  # We set the form to be our ExampleApp (interface)
    return form


def string2array(v):
    """Convert a string in an array"""
    try:
        v = complex(v) # if it is a number
        v = np.array([v])
        return v
    except:
        v = [complex(iv) for iv in v.split(",")]
        return np.array(v)
    return None


def array2string(v):
    """Convert an array to a string"""
    ss = ""
    ss += str(v[0])
    for i in range(1,len(v)): ss += ","+str(v[i])
    return ss


def get_array(name,v0=[0.,0.,0.],**kwargs):
    v = getattr(form,name).text() # get the text
    v = string2array(v) # convert to array
    if v is not None: return v # return the array
    else: # something wrong happened
        modify(name,array2string(v0)) # overwrite
        return np.array(v0) # return the default value


def get(name,string=False,default=0.0,call=True):
  """Return a certain value"""
  try:
      obj = getattr(form,name) # get the object
      out = obj.text()
      if string: return out # return as string
      try: # if it is a number
          return float(out) # return as float
      except: # execute
          if call:
              if "import os" in out: raise # silly sanity check
              out = out.replace("\n","")
              a = eval("lambda r: "+out) # execute the string
              # try the function
              try: 
                  a([0.,0.,0.])
                  return a
              except: raise
          else: raise
  except:
      if holler(): print(name,"not found, set to ",default)
      modify(name,default) # set this value
      return default



def getbox(name):
  try:
    obj = getattr(form,name) # get the object
    return str(obj.currentText()) # return the text
  except:
    if holler(): print(name,"not found, set to None")
    return None


def set_combobox(name,cs=[]):
    """Add the different colormaps to a combox"""
    try: cb = getattr(form,name)
    except:
        if holler(): print("Combobox",name,"not found")
        return
    cb.clear() # clear the items
    cb.addItems(cs)



def modify(name,text):
  try:
    obj = getattr(form,name) # get the object
    out = obj.setText(str(text))
    app.processEvents() # update the interface
  except: pass

set_value = modify

def is_checked(name,default=False):
    try:
        obj = getattr(form,name) # get the object
        return obj.isChecked()
    except: return default



def set_image(name,path):
  """Set a certain image"""
  label = getattr(form,name) # get the object
  pixmap = QPixmap(path)
  label.setPixmap(pixmap)
  label.show()


def set_logo(name,image):
  """Set a certain logo"""
  qlroot = os.path.dirname(os.path.realpath(__file__))+"/../../"
  path = qlroot+"/interface-pyqt/logos/"+image
  set_image(name,path)
  


def save_interface(self,output=None):
    if output is None: output = os.getcwd() + "/QH_save/interface.qh"
    obs = dir(self) # all the different objects
    out = dict() # dictionary
    for obj in obs: # loop over objects
        o = getattr(self,obj) # get this object
        if type(o)==QtWidgets.QLineEdit: # line object
            out[obj] = o.text() # save this info
    import json
    with open(output, 'w') as outf: # write as json file
        json.dump(out, outf)
#    load_interface(self,output)
        


def load_interface(self,inputfile):
    a_file = open(inputfile, "r")
    # this can be a bit dangerous
    out = eval(a_file.read()) # create a dictionary
    for obj in out: # loop over objects
        o = getattr(self,obj) # get this object
        if type(o)==QtWidgets.QLineEdit: # line object
            self.set(obj,out[obj]) # set this value in the interface
#    print(type(out))





def connect_signals(ds):
  for d in ds: # loop over names
    form.connect(self.pb, SIGNAL("clicked()"),self.button_click)



if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function



