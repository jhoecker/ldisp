#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import logging

class lTreeView(QtWidgets.QTreeView):
    """Tree view of Folders and LEEM images. Use only with
    QFileSystemModel"""
    newItemSelected = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QTreeView.__init__(self)
        self.clicked.connect(self.on_select)
        
    def setupView(self):
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        
    def on_select(self, indexItem):
        if self.model().isDir(indexItem):
            return
        else:
            self.newItemSelected.emit()
            
    def _selectedIndex(self):
        try: 
            currentIndex = self.selectionModel().selectedIndexes()[0]
        except IndexError:
            logging.debug('lTreeView:_selectedIndex: No item selected.')
            return
        return currentIndex
    
    def get_fname(self):
        currentIndex = self._selectedIndex()
        fname = self.model().filePath(currentIndex)
        return fname
        
    def selectPrevious(self):
        currentIndex = self._selectedIndex()
        if currentIndex is None: return
        if currentIndex.row() > 0:
            newIndex = self.indexAbove(currentIndex)
        else:
            logging.debug('Last element in index.')
            return
        self.clearSelection()
        self.selectionModel().select(newIndex, 
                                     QtCore.QItemSelectionModel.Select)
        self.scrollTo(newIndex, QtGui.QAbstractItemView.PositionAtTop)
        if not self.model().isDir(newIndex):
            self.newItemSelected.emit() 
        
    def selectNext(self):
        currentIndex = self._selectedIndex()
        if currentIndex is None: return
        if currentIndex.row() < self.model().rowCount(currentIndex.parent())-1:
            newIndex = self.indexBelow(currentIndex)
        else:     
            logging.debug('Last element in index.')
            return
        self.clearSelection()
        self.selectionModel().select(newIndex, 
                                     QtCore.QItemSelectionModel.Select)
        self.scrollTo(newIndex, QtGui.QAbstractItemView.PositionAtBottom)
        if not self.model().isDir(newIndex):
            self.newItemSelected.emit()

    def selectByFileName(self, fname):
        selectedIndex = self.model().index(fname)
        self.selectionModel().select(selectedIndex,
                                     QtCore.QItemSelectionModel.Select)
        self.newItemSelected.emit()
