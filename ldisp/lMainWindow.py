#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import logging
import os
import pyqtgraph as pg
import LEEMImage as li

from . import lMetaDataModel as lmdm
from . import lFileTreeView as lftv
from . import lconfig
 
class ldispMain(QtWidgets.QMainWindow):
    """ldisp Main Window"""
    leemImgChanged = QtCore.pyqtSignal()

    def __init__(self, fname):
        super(ldispMain, self).__init__()
        # create instance of metadata to set the default keys
        self.metadata = lmdm.MetaData()

        # global variables
        self.b_normCCD = False
        self.CCDimg = None
        self.leemImg = None
        self.filterLEED_sigma = 15

        filename = self.getPath(fname)
        self.leemImgChanged.connect(self.disp_lfile)

        self.initUI()

        #image file if given from cmd
        if (filename is not None and os.path.isfile(filename) is True):
            self.lTreeView.selectByFileName(fname)

    def initUI(self):

        self.setIconTheme()

        ## Widgets ##
        self.setCentralWidget(QtGui.QWidget(self))

        ## metaDataView
        self.createMetaDataView()

        ## LEEM Image View
        self.createImView()

        ## TreeView of Folder
        self.createFolderView()
        
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
        ## Setup toolbar
        toolbar = self.addToolBar('Tools')
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        # Add actions
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
                                    'Configure', self)
        configAction.triggered.connect(self.configure_dialog)
        ## shift config dialog to the right
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, 
                             QtGui.QSizePolicy.Expanding)

        ## Add actions to toolbar
        toolbar.addAction(openAction)
        toolbar.addAction(exitAction)
        toolbar.addAction(preImAction)
        toolbar.addAction(nextImAction)
        ## substract CCD ##
        self.normAction = QtGui.QAction(QtGui.QIcon.fromTheme('draw-circle'),
                'Subtract CCD', self)
        self.normAction.setCheckable(True)
        toolbar.addAction(self.normAction)
        self.getCCDMenu(self.normAction)
        self.normAction.triggered.connect(self.toggleCCD)
        ## filter inelastics
        self.filterInelastics = QtGui.QAction(QtGui.QIcon.fromTheme('antivignetting'),
                                              'Filter LEED', self)
        self.filterInelastics.setCheckable(True)
        toolbar.addAction(self.filterInelastics)
        self.filterInelastics.triggered.connect(self.toggle_filter_LEED)
        ## align config dialog on right hand side
        toolbar.addWidget(spacer)
        toolbar.addAction(configAction)

    def createFolderView(self):
        """Sets up the folder view and the corresponding filesystem model"""
        self.lTreeView = lftv.lTreeView()

        # Set Model
        self.fmodel = QtWidgets.QFileSystemModel(self.lTreeView)
        self.fmodel.setRootPath(self.currentPath)
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
        self.lTreeView.setRootIndex(self.fmodel.index(self.currentPath))
        self.lTreeView.setupView()
        self.lTreeView.newItemSelected.connect(self.getLEEMImg)

    def createImView(self):
        self.lImView = pg.ImageView()

    def open_folder(self):
        # FIXME QFileDialog widget seems not to expand the folders in Qt5
        dname = QtWidgets.QFileDialog.getExistingDirectory(self,
                'Select Directory',
                self.currentPath,
                QtWidgets.QFileDialog.ShowDirsOnly)
        if not dname:
            return
        else:
            self.currentPath = dname
        self.fmodel.setRootPath(self.currentPath)
        self.lTreeView.setRootIndex(self.fmodel.index(self.currentPath))
        self.lTreeView.sortByColumn(0,0)
        
    def configure_dialog(self):
        self.configDialog = lconfig.ConfDialog(self.metadata.currentKeys)
        if self.configDialog.exec_() == QtGui.QDialog.Accepted:
            newKeys = self.configDialog.getMetaDataKeys()
            self.filterLEED_sigma = self.configDialog.getSigma()
            self.metadata.setCurrentKeys(newKeys)
        # Load new data model if one is set after the keys were changed
        if self.metaDataListView.model() is not None:
            self.metaDataListView.setModel(
                    lmdm.lMetaDataModel(
                            self.metadata.getDispedData(),
                            self.metaDataListView))

    def getLEEMImg(self, *args, **karwgs):
        """Import LEEM image from path given by parameter or from tree view"""
        if args:
            fname = args[0]
        else:
            fname = self.lTreeView.get_fname()
        self.leemImg = li.LEEMImage(fname)
        logging.debug('getLEEMImg: b_normCCD is {}'.format(self.b_normCCD))
        if self.b_normCCD is True:
            try:
                self.leemImg.data = self.leemImg.normalizeOnCCD(self.CCDimg)
            except li.DimensionError:
                msgbx = QtGui.QMessageBox()
                msgbx.setText('Dimensions of image and CCD image do not match.')
                msgbx.setIcon(QtGui.QMessageBox.Warning)
                msgbx.exec_()
                self.CCDimg = None
                self.setNormState(False)
        self.leemImgChanged.emit()

    def disp_lfile(self):
        """Displays LEEM images in pyqtgraph widget"""
        self.lImView.setImage(self.leemImg.data)
        self.metadata = lmdm.MetaData(self.leemImg.metadata)
        ## To avoid QTimer-Errors add parents (the views) to the models
        ## see http://stackoverflow.com/questions/30549477/
        ##         pyqt-qcombobox-with-qstringmodel-cause-
        ##         qobjectstarttimer-qtimer-can-only-be
        self.metaDataListView.setModel(
                lmdm.lMetaDataModel(
                        self.metadata.getDispedData(),
                        self.metaDataListView))

    def getPath(self, fname=None):
        if fname is None:
            self.currentPath = os.path.curdir
        elif os.path.isfile(fname):
            fname = os.path.abspath(fname)
            self.currentPath = os.path.dirname(fname)
        elif os.path.isdir(fname):
            self.currentPath = os.path.abspath(fname)
        else:
            logging.error('No directory of file given')
            self.currentPath = os.path.curdir
        return fname

    def setNormState(self, state):
        self.b_normCCD = state
        self.normAction.setChecked(state)

    def toggleCCD(self):
        logging.debug(('lMainWindow: toggleCCD: normAction is {}, ' +
                'b_normCCD is {}').format(self.normAction.isChecked(),
                                         self.b_normCCD))
        if self.normAction.isChecked():
            self.b_normCCD = True
        else:
            self.b_normCCD = False
        if self.b_normCCD is True and self.CCDimg == None:
            self.loadCCD()
        try:
            self.getLEEMImg()
        except TypeError:
            logging.debug('toggleCCD: TypeError exception raised')
            pass

    def loadCCD(self):
        fnameCCD = QtGui.QFileDialog.getOpenFileName(self,
                'Open CCD File',
                self.currentPath,
                'Data Files (*.dat)')[0]
        if not fnameCCD and self.CCDimg == None:
            self.setNormState(False)
            return
        self.CCDimg = li.LEEMImage(fnameCCD)
        logging.debug('lMainWindow: loadCCD: CCD loaded')

    def getCCDMenu(self, menuAction):
        menuCCD = QtGui.QMenu()
        menuAction.setMenu(menuCCD)
        getCCD = menuCCD.addAction('Open CCD image')
        getCCD.setIcon(QtGui.QIcon.fromTheme('folder-pictures-symbolic'))
        getCCD.triggered.connect(self.loadCCD)

    def toggle_filter_LEED(self):
        filterState = self.filterInelastics.isChecked()
        logging.debug('lMainWindow toggle_filter_LEED: filterState = {}'
                .format(filterState))
        if filterState is True:
            self.leemImg.data = self.leemImg.filterInelasticBkg(15)
            self.disp_lfile()
        else:
            self.getLEEMImg()

    def setIconTheme(self):
        de = os.environ.get('DESKTOP_SESSION').lower()
        if de.__contains__('plasma5'):
            pass
        elif de.__contains__('lxde'):
            QtGui.QIcon.setThemeName('nuoveXT2')
