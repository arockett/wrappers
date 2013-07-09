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

    def create_window(self):
        return ChamviewWindow(self.base_command, self.args, self.options)

class ChamviewWindow(OptionInputWindow):

    def fill_command(self):
        return QVBoxLayout()

    def fill_body(self):
        # Create boxes to add Widgets to
        self.body = QHBoxLayout()
        arg_box = QVBoxLayout()
        frame_grab_box = QVBoxLayout()

        # Add Image Directory widget w/ frame grab potential

        # Add all other widgets
        arg_names = [x[0] for x in self.args]
        for opt in self.options:
            if opt[0] == 'Image Directory': continue
            i = arg_names.index(opt[0])
            blueprint, required = self.parse_arg(self.args[i][1])
            widget = self.make_widget(blueprint, required, opt)
            arg_box.addWidget(widget)

        # Pack self.body
        frame_grab_box.addStretch()
        self.body.addLayout(arg_box)
        self.body.addWidget(self.vert_line())
        self.body.addLayout(frame_grab_box)
        return self.body


def main():
    '''Open a ChamviewWrapper.'''
    os.chdir('../chamview')
    wrapper = ChamviewWrapper()
    wrapper.wrap()

if __name__ == '__main__':
    sys.exit(main())
