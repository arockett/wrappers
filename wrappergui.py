#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Gui used by CLIWrapper to get user inputted options.'''

import os
from Tkinter import *
import tkFileDialog

class OptionInputGui:
    
    def __init__(self,command,args,options):
        self.command = command
        self.args = args
        self.options = options
      
        self.root = Tk()
        
        body = Frame(self.root)
        self.body(body)
        body.pack(padx=5,pady=5)
        
        self.root.protocol("WM_DELETE_WINDOW",self.root.cancel)
        
        self.result = self.command, self.args, self.options
        
        self.root.mainloop()
            
#****** Create GUI ******
            
    def body(self,master):
        # Fill Option Frame
        opt_frame = Frame(master)
        for opt in options:
            blueprint = self.parse_arg(opt[1])
            if len(blueprint) == 1:
                continue
            elif blueprint[1] == '':
                opt[2] = StringVar()
                self.new_string(opt_frame,opt[0],opt[2])
            elif blueprint[1][0] == '_file_':
                opt[2] = StringVar()
                self.new_file(opt_frame,opt[0],blueprint[1][1:],opt[2])
            elif blueprint[1][0] == '_dir_':
                opt[2] = StringVar()
                self.new_directory(opt_frame,opt[0],opt[2])
            elif blueprint[1][0] == '_int_':
                pass
            elif blueprint[1][0] == '_double_':
                pass
            else:
                pass
        opt_frame.pack()
        
        #Make buttonbox
        self.buttonbox(master)
                    
    def parse_arg(self,raw):
        result = raw
        if ':' in result:
            result = result.split(':')
            if len(result) > 1 and l[1] != '':
                result[1] = result[1].split(',')
        return result
        
    def new_bool
                
    def new_string(self,master,name,var):
        box = Frame(master)
        
        label = Label(box, text=name)
        label.pack(padx=5)
        
        entry = Entry(box, width=20, relief=SUNKEN, textvariable=var)
        entry.pack(padx=5,pady=10)
        
        box.pack()
        
    def new_file(self,master,name,ext=[('All Types','*')],var):
        box = Frame(master)
        
        label = Label(box, text=name)
        label.pack(padx=5)
        
        entry = Entry(box, width=20, relief=SUNKEN, textvariable=var)
        entry.bind("<Button-1>", lambda x: self.select_file(ext))
        entry.pack(padx=5,pady=10)
        
        box.pack()
        
    def select_file(self,extensions,event=''):
        path = tkFileDialog.askopenfilename(filetypes=extensions,
                                            initialdir=os.getcwd(),
                                            title='Choose File')
        if path:
            widget.delete(0,END)
            widget.insert(0,path)
            
    def new_directory(self,master,name,var):
        box = Frame(master)
        
        label = Label(box, text=name)
        label.pack(padx=5)
        
        entry = Entry(box, width=20, relief=SUNKEN, textvariable=var)
        entry.bind("<Button-1>", self.select_dir)
        entry.pack(padx=5,pady=10)
        
        box.pack()
        
    def select_file(self,event=''):
        path = tkFileDialog.askdirectory(initialdir=os.getcwd(),
                                         title='Choose Directory')
        if path:
            widget.delete(0,END)
            widget.insert(0,path)
        
    def new_menu(self,master,name,opts=[],var):
        pass
        
    def new_int(self,master,name,var):
        pass
        
    def new_double(self,master,name,var):
        pass
            
    def buttonbox(self,master):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(master)

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
        self.command = self.cmd.get()
        for opt in self.options:
            opt[2] = opt[2].get()
            if not isinstance(opt[2],bool):
                opt[2] = str(opt[2])
            
        self.result = self.command, self.args, self.options
            

