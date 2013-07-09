#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Chamview Gui used by CLIWrapper to get user inputted options for Chamview.'''

import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cliwrapper import CLIWrapper
from cligui import OptionInputWindow

class ChamviewWrapper(CLIWrapper):

    def __init__(self):
        command = 'python chamview.py'
        args = [('Image Directory', '-d:_dir_|*'),
                ('Existing Points File', '-p:_file_:Text File,*.txt'),
                ('Output File', '-o:_file_:Text File,*.txt'),
                ('Preprocessor', '-i:_menu_:'),
                ('Chooser', '-c:_menu_:BasicGui'),
                ('System Info File', '-w:_file_:Text File,*.txt')]
        CLIWrapper.__init__(self, command, args)

    #def create_window(self):
    #    return ChamviewWindow(self.base_command, self.args, self.options)

class ChamviewWindow(OptionInputWindow):

    #def fill_command(self):
    #    pass

    def fill_body(self):
        OptionInputWindow.fill_body(self)

    # Might not need to override this func, we'll see
    #def apply(self):
    #    pass


def main():
    '''Open a ChamviewWrapper.'''
    os.chdir('../chamview')
    wrapper = ChamviewWrapper()
    wrapper.wrap()

if __name__ == '__main__':
    sys.exit(main())
