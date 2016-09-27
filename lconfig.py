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
        
        ii = 0
        for item in metaDataKeys:
            ## Use list with strings to create checkboxes
            layout.addWidget(QtWidgets.QCheckBox(item), ii-ii%2,ii%2)
            ii += 1
        #layout.setColumnStretch(ii, 1)
        #layout.setRowStretch(ii,2)
        layout.addWidget(self.btn_ok, ii, 1, 1, 1)
        layout.addWidget(self.btn_cnl, ii, 2, 1, 1)
        self.setLayout(layout)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Configuration')
        
        
        
