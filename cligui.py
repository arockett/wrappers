#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Gui used by CLIWrapper to get user inputted options.'''

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class OptionInputWindow(QMainWindow):

    def __init__(self, command, args, options, *extra):
        self.command = QString(command)
        self.args = args
        self.options = options
        self.required = []
        apply(QWidget.__init__, (self, ) + extra)

        widget = self.new_tab()
        self.setWindowTitle("Parameter Manager")
        self.setCentralWidget(widget)

        self.result = self.command, self.args, self.options

    def new_tab(self):
        widget = QWidget()
        layout = QGridLayout()

        # Create widget to edit the command
        layout.addLayout(self.fill_command(),0,0)
        # Horizontal line
        layout.addWidget(self.horizontal_line(),1,0)
        # Create widgets for each option
        layout.addLayout(self.fill_body(),2,0)
        # Horizontal line
        layout.addWidget(self.horizontal_line(),3,0)
        # Make buttonbox
        layout.addLayout(self.fill_buttonbox(),4,0)

        widget.setLayout(layout)
        return widget

#****** Create GUI ******

    def horizontal_line(self):
        # Horizontal line
        hline = QFrame()
        hline.setFrameStyle( QFrame.HLine | QFrame.Raised )
        hline.setLineWidth(3)
        hline.setMidLineWidth(3)
        return hline

    def vert_line(self):
        # Vertical line
        vline = QFrame()
        vline.setFrameStyle( QFrame.VLine | QFrame.Raised )
        vline.setLineWidth(3)
        vline.setMidLineWidth(3)
        return vline

    def fill_command(self):
        box = QVBoxLayout()
        # Create widget for the command
        box.addWidget(QLabel('Command'),0)
        command_edit = self.new_string(self.command)
        command_edit.setText(self.command)
        command_edit.selectAll()
        box.addWidget(command_edit)
        return box

    def fill_body(self):
        self.body = QHBoxLayout()
        arg_box = QHBoxLayout()
        #boolean_box = QVBoxLayout()
        #boolean_box.addWidget(QLabel("Boolean Options"))
        num_of_columns = int(len(self.options) / 6.0 + 1)
        if len(self.options) % 6 == 0:
            num_of_columns -= 1

        columns = []
        for i in range(num_of_columns):
            columns.append(QVBoxLayout())
        # Create widgets for each option
        num = -1    # use to track which column to add the widget to
        arg_names = [x[0] for x in self.args]  # use to get the widget blueprint
        for opt in self.options:
            num += 1
            index = int(num / 6.0)
            i = arg_names.index(opt[0])
            blueprint, req = self.parse_arg(self.args[i][1])
            if len(blueprint) == 1:
                opt[2] = False
                check = not req
                columns[index].addWidget(self.new_bool(opt,check))
                #num -= 1
            elif blueprint[1] == '':
                opt[2] = QString('')
                widget = self.add_group(opt[0],widget=self.new_string(opt),optional=req)
                columns[index].addWidget(widget)
            elif blueprint[1] == '_file_':
                opt[2] = QString('')
                try:
                    filetypes = [tuple(ft.split(',')) for ft in blueprint[2:]]
                    filetype_str = ''
                    for typ in filetypes:
                        filetype_str += typ[0]+' ('
                        for ext in typ[1:]:
                            filetype_str += ext + ' '
                        filetype_str = filetype_str[:-1] + ')'
                        filetype_str += ';;'
                    filetype_str = filetype_str[:-2]
                    widget = self.add_group(opt[0],layout=self.new_file(opt,filetype_str),optional=req)
                except IndexError:
                    widget = self.add_group(opt[0],layout=self.new_file(opt),optional=req)
                columns[index].addWidget(widget)
            elif blueprint[1] == '_dir_':
                opt[2] = QString()
                widget = self.add_group(opt[0],layout=self.new_directory(opt),optional=req)
                columns[index].addWidget(widget)
            elif blueprint[1] == '_int_':
                box = QHBoxLayout()
                box.addSpacing(15)
                try:
                    min_,max_,step = blueprint[2],blueprint[3],blueprint[4]
                    box.addWidget(self.new_int(opt,min_,max_))
                except IndexError:
                    box.addWidget(self.new_int(opt))
                widget = self.add_group(opt[0],layout=box,optional=req)
                columns[index].addWidget(widget)
            elif blueprint[1] == '_float_':
                box = QHBoxLayout()
                box.addSpacing(15)
                try:
                    min_,max_,step = blueprint[2],blueprint[3],blueprint[4]
                    box.addWidget(self.new_float(opt,min_,max_))
                except IndexError:
                    box.addWidget(self.new_float(opt))
                widget = self.add_group(opt[0],layout=box,optional=req)
                columns[index].addWidget(widget)
            elif blueprint[1] == '_menu_':
                opt[2] = QString('')
                try:
                    choices = blueprint[2:]
                    widget = self.add_group(opt[0],widget=self.new_menu(opt,choices),optional=req)
                except IndexError:
                    widget = self.add_group(opt[0],widget=self.new_menu(opt),optional=req)
                columns[index].addWidget(widget)

        # Make partially filled Boxes look nicer
        columns[-1].addStretch()
        #boolean_box.addStretch()
        # Fill arg_box with the columns
        for col in columns:
            arg_box.addLayout(col)
            arg_box.addWidget(self.vert_line())

        self.body.addLayout(arg_box)
        #self.body.addLayout(boolean_box)
        #self.body.addSpacing(50)
        return self.body

    def parse_arg(self,raw):
        if raw[-2:] == '|*':
            optional = False
            raw = raw[:-2]
        else:
            optional = True
        if ':' in raw:
            result = raw.split(':')
        else:
            result = [raw]
        return result, optional

    def add_group(self,name,widget=None,layout=None,optional=True):
        group = QGroupBox(name)
        group.setCheckable(optional)
        if not optional:
            self.required.append(name)
        group.setFlat(True)
        if optional:
            group.setChecked(False)
        box = QVBoxLayout()
        if widget:
            box.addWidget(widget)
        if layout:
            box.addLayout(layout)
        group.setLayout(box)
        #self.connect(group, SIGNAL("mousePressEvent(QMouseEvent)"),
        #            group, SLOT("setChecked(True)"))
        #group.toggled.connect(edit_widget)
        return group

    def store_value(self,index,value):
        print value
        print type(value)
        if isinstance(value, QString):
            self.options[index][2].swap(value)
        else:
            self.options[index][2] = value

    def new_bool(self,obj,checked=False):
        checkbox = QCheckBox(obj[0])
        if checked:
            checkbox.setChecked(checked)
            checkbox.stateChanged.connect(lambda: checkbox.setCheckState(2))
        else:
            store = lambda: self.store_value(self.options.index(obj),checkbox.isChecked())
            checkbox.stateChanged.connect(store)
        return checkbox

    def new_string(self,obj):
        qedit = QLineEdit('')
        if not isinstance(obj,QString):
            store = lambda: self.store_value(self.options.index(obj),qedit.text())
        else:
            store = lambda s=qedit.text(): self.command.swap(s)
        qedit.textChanged.connect(store)
        return qedit

    def new_file(self,obj,ext='All Types (*)'):
        box = QHBoxLayout()

        qedit = QLineEdit('')
        store = lambda: self.store_value(self.options.index(obj),qedit.text())
        qedit.textChanged.connect(store)
        browse = QPushButton('Browse')
        browse.clicked.connect(lambda: self.select_file(qedit,ext))

        box.addWidget(qedit)
        #box.addSeparator(2)
        box.addWidget(browse)
        return box

    def select_file(self,ledit,extensions):
        path = QFileDialog.getOpenFileName(None,QString("Select File"),
                                                QString(os.getcwd()),
                                                QString(extensions))
        if path:
            # Account for spaces in the path
            dirs = str(path).split('/')
            for i in range(len(dirs)):
                for ch in dirs[i]:
                    if ch.isspace():
                        dirs[i] = '"'+dirs[i]+'"'
            path = QString('/'.join(dirs))

            ledit.setText(path)

    def new_directory(self,obj):
        box = QHBoxLayout()

        qedit = QLineEdit('')
        store = lambda: self.store_value(self.options.index(obj),qedit.text())
        qedit.textChanged.connect(store)
        browse = QPushButton('Browse')
        browse.clicked.connect(lambda: self.select_dir(qedit))

        box.addWidget(qedit)
        #box.addSeparator(2)
        box.addWidget(browse)

        return box

    def select_dir(self,ledit):
        path = QFileDialog.getExistingDirectory(None,QString('Select Directory'),
                                                     QString(os.getcwd()),
                                                     QFileDialog.ShowDirsOnly)
        if path:
            # Account for spaces in the path
            dirs = str(path).split('/')
            for i in range(len(dirs)):
                for ch in dirs[i]:
                    if ch.isspace():
                        dirs[i] = '"'+dirs[i]+'"'
            path = QString('/'.join(dirs))

            ledit.setText(path)

    def new_int(self,obj,min_=None,max_=None,step=1):
        intspin = QSpinBox()
        if min_:
            intspin.setMinimum(int(min_))
        if max_:
            intspin.setMaximum(int(max_))
        intspin.setSingleStep(int(step))
        store = lambda: self.store_value(self.options.index(obj),intspin.value())
        intspin.valueChanged.connect(store)
        store()
        return intspin


    def new_float(self,obj,min_=None,max_=None,step=0.1):
        doublespin = QDoubleSpinBox()
        if min_:
            doublespin.setMinimum(float(min_))
        if max_:
            doublespin.setMaximum(float(max_))
        doublespin.setSingleStep(float(step))
        store = lambda: self.store_value(self.options.index(obj),doublespin.value())
        doublespin.valueChanged.connect(store)
        store()
        return doublespin

    def new_menu(self,obj,opts=[]):
        menu = QComboBox()
        for opt in opts:
            menu.addItem(opt,0)
        store = lambda: self.store_value(self.options.index(obj),menu.currentText())
        menu.currentIndexChanged.connect(store)
        return menu

    def fill_buttonbox(self):
        box = QHBoxLayout()

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save)
        run_button = QPushButton('Run')
        run_button.clicked.connect(self.run)

        box.addWidget(save_button)
        box.addStretch()
        box.addWidget(run_button)

        return box

#****** Standard Button Semantics ******

    def save(self):
        '''Store entered option and tell the cliwrapper to
        save the command and the options.'''
        if not self.validate():
            return

        self.apply()
        self.emit(SIGNAL("readyToSave()"))

    def open(self):
        '''Tell the cliwrapper to open the selected ".command" file.'''
        filename = ''

        self.emit(SIGNAL("readyToOpen(QString)"))

    def run(self, event=''):
        '''Store entered options and tell the cliwrapper to
        run the command with those options.'''
        if not self.validate():
            return

        self.apply()
        self.emit(SIGNAL("readyToRun()"))

    def cancel(self, event=''):
        # Close window
        self.result = None

    def validate(self):
        return True

    def apply(self):
        # Get indices in self.options of active options
        opt_names = [opt[0] for opt in self.options]
        indices = []
        for name in self.required:
            indices.append(opt_names.index(name))
        for box in self.body.children():      # arg_box and boolean_box
            print box
            for i in range(box.count()):      # column in arg_box, check boxes in bool_box
                item = box.itemAt(i)
                print item
                if isinstance(item, QVBoxLayout):
                    for i in range(item.count()): # search through columns
                        widget = item.itemAt(i).widget()
                        print widget
                        if isinstance(widget, QCheckBox):   # get indices of check boxes in bool_box
                            indices.append(opt_names.index(widget.text()))
                        elif isinstance(widget, QGroupBox): # get indices of active groups
                            if widget.isChecked():
                                indices.append(opt_names.index(widget.title()))

        # Grab the active arguments from self.options to use in the command
        opts = []
        for i in range(len(self.options)):
            if i in indices:
                opt = self.options[i]
                if not isinstance(opt[2], bool):
                    opts.append([opt[0],opt[1],str(opt[2])])
                else:
                    opts.append([opt[0],opt[1],opt[2]])
        print self.command
        print self.args
        print opts
        self.result = str(self.command), self.args, opts


