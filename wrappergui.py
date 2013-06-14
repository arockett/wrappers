#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Gui used by CLIWrapper to get user inputted options.'''

from Tkinter import *

class OptionInputGui:
    
    def __init__(self,command,args,options):
        self.command = command
        self.args = args
        self.options = options
      
        self.root = Tk()
        
        body = Frame(self.root)
        self.body(body)
        body.pack(padx=5,pady=5)
        
        self.root.protocol("WM_DELETE_WINDOW",self.cancel)
        
        self.result = self.command,self.args,self.options
        
        self.root.mainloop()
            
#****** Create GUI ******
            
    def body(self,master):
        pass
        
    def new_string(self):
        pass
        
    def new_path(self):
        pass
        
    def new_menu(self):
        pass
        
    def new_int(self):
        pass
        
    def new_double(self):
        pass
            
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self.root)

        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=RIGHT, padx=5, pady=5)
        w = Button(box, text="Run", width=10, command=self.run, default=ACTIVE)
        w.pack(side=RIGHT,padx=5, pady=5)

        self.root.bind("&lt;Return>", self.ok)
        self.root.bind("&lt;Escape>", self.cancel)

        box.pack()
        
#****** Standar Button Semantics ******
        
    def run(self, event=''):
        # Store entered options and run command with those options
        if not self.validate():
            return
            
        self.root.withdraw()
        self.root.update_idletasks()
        
        self.apply()
        
        self.cancel()
        
    def cancel(self, event=''):
        # Close window
        self.root.quit()
        
    def validate(self):
        return 1
        
    def apply(self):
        raise NotImplementedError
            

