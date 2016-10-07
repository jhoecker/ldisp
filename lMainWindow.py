#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import logging
import os
import pyqtgraph as pg
import LEEMImg as li
import lMetaDataModel as lmdm
import lFileTreeView as lftv
import lconfig
 
class ldispMain(QtWidgets.QMainWindow):

    def __init__(self, fname):
        super(ldispMain, self).__init__()
        self.initUI(fname)
        # create instance of metadata to set the default keys
        self.metadata = lmdm.MetaData()

    def initUI(self, fname):

        self.setIconTheme()

        ## Widgets ##
        self.setCentralWidget(QtGui.QWidget(self))

        ## metaDataView
        self.createMetaDataView()

        ## LEEM Image View
        self.createImView()

        ## TreeView of Folder
        self.createFolderView(fname)
        
        ## Toolbar
        # The toolbar has to be created after the folder view since it depends
        # on methods initialized in lTreeView.
        self.createToolbar()

        ## Layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.metaDataGroup, 0, 0, 1, 1)
        layout.addWidget(self.lTreeView, 1, 0, 1, 1)
        layout.addWidget(self.lImView, 0, 1, 2, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        self.centralWidget().setLayout(layout)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, 900, 500)
        self.setWindowTitle('ldisp - LEEM image viewer')

    def createMetaDataView(self):
        self.metaDataGroup = QtGui.QGroupBox('Meta Data')
        ## FIXME Alignment does not affect title
        # Bug in Qt?
        self.metaDataGroup.setAlignment(QtCore.Qt.AlignLeft)
        self.metaDataBox = QtGui.QVBoxLayout()
        self.metaDataListView = QtWidgets.QListView()
        self.metaDataBox.addWidget(self.metaDataListView)
        self.metaDataGroup.setLayout(self.metaDataBox)

    def createToolbar(self):
        ## exit
        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('application-exit'), 
                                   'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        ## open file
        openAction = QtGui.QAction(QtGui.QIcon.fromTheme('document-open'), 
                                   'Open Folder', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.open_folder)
        ## next file
        nextImAction = QtGui.QAction(QtGui.QIcon.fromTheme('go-next'), 
                                     'Next image', self)
        nextImAction.triggered.connect(self.lTreeView.selectNext)
        ## previous file
        preImAction = QtGui.QAction(QtGui.QIcon.fromTheme('go-previous'),
                                    'Previous image', self)
        preImAction.triggered.connect(self.lTreeView.selectPrevious)
        ## configuration dialog
        configAction = QtGui.QAction(QtGui.QIcon.fromTheme('configure'),
                                    'Configure View', self)
        configAction.triggered.connect(self.configure_View)
        ## shift config dialog to the right
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, 
                             QtGui.QSizePolicy.Expanding)
        ## Setup Toolbar
        toolbar = self.addToolBar('Tools')
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toolbar.addAction(openAction)
        toolbar.addAction(exitAction)
        toolbar.addAction(preImAction)
        toolbar.addAction(nextImAction)
        toolbar.addWidget(spacer)
        toolbar.addAction(configAction)

    def createFolderView(self, fname):
        """Sets up the folder view and the corresponding filesystem model"""
        self.lTreeView = lftv.lTreeView()
        # Check if given path is file or folder
        if fname is None:
            path = os.path.curdir
        elif os.path.isfile(fname):
            fname = os.path.abspath(fname)
            path = os.path.dirname(fname)
            self.disp_lfile(fname)
        elif os.path.isdir(fname):
            path = os.path.abspath(fname)
        else:
            logging.error('No directory of file given')
            path = os.path.curdir

        # Set Model
        self.fmodel = QtWidgets.QFileSystemModel(self.lTreeView)
        self.fmodel.setRootPath(path)
        # Filter out all files without extension .dat
        self.fmodel.setFilter(QtCore.QDir.Filter(
            QtCore.QDir.Dirs | QtCore.QDir.Files |
            QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot))
        nameFilter = ['*.dat']
        self.fmodel.setNameFilters(nameFilter)
        self.fmodel.setNameFilterDisables(False)
        self.fmodel.sort(0)

        ## Setup View
        self.lTreeView.setModel(self.fmodel)
        self.lTreeView.setRootIndex(self.fmodel.index(path))
        self.lTreeView.setupView()
        self.lTreeView.newItemSelected.connect(self.disp_lfile)

    def createImView(self):
        self.lImView = pg.ImageView()

    def open_folder(self):
        dname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.fmodel.setRootPath(dname)
        self.lTreeView.setRootIndex(self.fmodel.index(dname))
        self.lTreeView.sortByColumn(0,0)
        
    def configure_View(self):
        self.configDialog = lconfig.ConfDialog(self.metadata.currentKeys)
        # FIXME Use QDialog.Accept or something similar.
        # Using .exec_ == 1024 is just a workaround
        if self.configDialog.exec_() == 1024:
            newKeys = self.configDialog.getMetaDataKeys()
            self.metadata.setCurrentKeys(newKeys)
        # Load new data model if one is set after the keys were changed
        if self.metaDataListView.model() is not None:
            self.metaDataListView.setModel(lmdm.lMetaDataModel(self.metadata.getDispedData(),
                                                               self.metaDataListView))
 
    def disp_lfile(self, *args, **karwgs):
        """Displays LEEM images in pyqtgraph widget"""
        if args:
            fname = args[0]
        else:
            fname = self.lTreeView.get_fname()
        leem_img = li.UKSoftImg(fname)
        self.lImView.setImage(leem_img.data)
        self.metadata = lmdm.MetaData(leem_img.metadata)
        ## To avoid QTimer-Errors add parents (the views) to the models
        ## see http://stackoverflow.com/questions/30549477/
        ##         pyqt-qcombobox-with-qstringmodel-cause-
        ##         qobjectstarttimer-qtimer-can-only-be
        self.metaDataListView.setModel(lmdm.lMetaDataModel(self.metadata.getDispedData(),
                                                           self.metaDataListView))

    def setIconTheme(self):
        de = os.environ.get('DESKTOP_SESSION').lower()
        if de.__contains__('plasma5'):
            pass
        elif de.__contains__('lxde'):
            QtGui.QIcon.setThemeName('nuoveXT2')
