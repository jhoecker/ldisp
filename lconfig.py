#!/usr/share/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class ConfDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        metaDataKeys = ['FOV', 'Start Voltage', 'Sample Temp.', 'Main',
                        'timestamp', 'test']
        
        layout = QtGui.QGridLayout()
        self.btn_ok = QtGui.QPushButton('Ok', self)
        self.btn_cnl = QtGui.QPushButton('Cancel', self)
        
        for item in metaDataKeys:
            ## Use list with strings to create checkboxes
            pass
        
        tt = QtWidgets.QCheckBox('Test')
        
        
        
        layout.setColumnStretch(1, 2)
        layout.setRowStretch(1,2)
        
        layout.addWidget(tt, 1,2)
        
        layout.addWidget(self.btn_ok, 3, 3, 1, 1)
        
        layout.addWidget(self.btn_cnl, 3, 4, 1, 1)
        self.setLayout(layout)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Configuration')
        
        
        
